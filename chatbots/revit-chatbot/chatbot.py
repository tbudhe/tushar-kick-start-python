import os
from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime, date
load_dotenv()
client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
system_prompt = """You are a helpful assistant for Autodesk Revit questions. Keep answers short and practical."""
system_prompt_ttft = """You are a helpful assistant for Autodesk Revit questions. Keep answers short and practical.

Autodesk Revit is a building information modeling (BIM) software used by architects, structural engineers, MEP engineers, designers and contractors. It allows users to design a building and structure, and its components in 3D, annotate the model with 2D drafting elements, and access building information from the building model's database. Revit is 4D BIM capable, with tools to plan and track various stages in the building's lifecycle, from concept to construction and later demolition. In Revit, an element is any object you can select and modify — from a simple wall or door to a complex parametric family. Every element belongs to a category, a family, and a type. Categories group similar elements such as Walls, Doors, Windows, and Rooms. Families are the templates that define the geometry and parameters of an element. A family can have multiple types, each with different parameter values such as size or material. Instance parameters apply to a single placed element, while type parameters apply to all instances of that type simultaneously.

The Revit interface is organized around a ribbon that changes contextually based on what you select or what tool you activate. The Project Browser on the left side of the screen lets you navigate views, legends, schedules, sheets, and families. The Properties palette shows the parameters of the currently selected element or, when nothing is selected, the parameters of the active view. The View Control Bar at the bottom of each view lets you control the scale, detail level, visual style, and other display settings. Most editing commands in Revit operate on selections: you first select one or more elements, then apply a command from the ribbon or context menu. Revit supports multi-select using Ctrl+click, and filter-selection using the Filter tool in the status bar. You can also use a crossing window (right-to-left drag) or an enclosing window (left-to-right drag) to select multiple elements at once.

Walls in Revit are system families, meaning their definitions live in the project itself rather than in an external family file. A wall's structure is defined by its layers — a sequence of materials with assigned thicknesses and functions such as Structure, Thermal/Air Layer, or Finish. You edit wall structure through the Type Properties dialog under the Edit button next to the Structure field. Walls can be attached to floors, roofs, and ceilings so that their tops follow the host geometry automatically; use the Attach Top/Base command on the Modify | Walls tab to establish this relationship. Curtain walls are a special wall category in Revit that model glazed facades. They consist of a grid of mullions and panels; the grid spacing can be fixed, variable, or driven by a rule. Individual panels can be replaced with different panel families including doors and windows, making curtain walls highly flexible for complex facade designs.

Revit schedules are tabular views that extract parameter data from elements in the model. A schedule is created from the View tab → Schedules → Schedule/Quantities. In the New Schedule dialog you choose the category you want to report, then add fields (parameters) and configure sorting, grouping, and filtering. Calculated fields let you derive new values from existing parameters using Revit's formula language, which supports basic arithmetic and several built-in functions. Schedules update automatically when the model changes — editing a parameter value in the schedule writes it back to the element, and vice versa. Key schedules are a special type used to drive instance parameters of multiple elements simultaneously; they are particularly useful for assigning room finishes or door hardware sets across a project. Schedule appearance is controlled on the Formatting and Appearance tabs of the Schedule Properties dialog, where you can set column widths, header text, font styles, and grid lines before placing the schedule on a sheet.
"""

conversation = [
    {"role": "user", "content": "How do I add a door in Revit?"},
    {"role": "assistant",  "content": "Architecture tab → Door (or press DR). Click a wall to place it. Set position with temporary dimensions."},
    {"role": "user", "content": "How do I change a wall's height?"},
    {"role": "assistant", "content": "Select the wall → Properties panel → set Unconnected Height. Or attach its top to a level."},
]


def ask(user_input):
    conversation.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=200,
        system=system_prompt,
        messages=conversation  # send the full history, not just the latest message
    )

    reply = next(
        block.text for block in response.content if block.type == "text")
    # save the reply too
    conversation.append({"role": "assistant", "content": reply})
    return reply


def ask_streaming(user_input):
    conversation.append({"role": "user", "content": user_input})
    now = datetime.now()
    print("current time: ", now)  # Output: 2026-07-23 11:10:00.123456
    full_reply = ""
    with client.messages.stream(
        model="claude-sonnet-5",
        max_tokens=500,
        system=system_prompt,
        messages=conversation
    ) as stream:
        for text_chunk in stream.text_stream:
            # print as it arrives, no newline
            print(text_chunk, end="", flush=True)
            full_reply += text_chunk

    conversation.append({"role": "assistant", "content": full_reply})
    return full_reply

def ask_streaming_ttft(user_input):
    conversation.append({"role": "user", "content": user_input})

    start = datetime.now()
    first_chunk_seen = False
    full_reply = ""

    with client.messages.stream(
        model="claude-sonnet-5",
        max_tokens=500,
        system=system_prompt_ttft,
        messages=conversation
    ) as stream:
        for text_chunk in stream.text_stream:
            if not first_chunk_seen:
                ttft = (datetime.now() - start).total_seconds()
                print(f"\n[TTFT: {ttft:.2f}s]")
                first_chunk_seen = True
            print(text_chunk, end="", flush=True)
            full_reply += text_chunk

    conversation.append({"role": "assistant", "content": full_reply})
    return full_reply


while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    print("Assistant: ", end="")
    ask_streaming_ttft(user_input)
    print()
