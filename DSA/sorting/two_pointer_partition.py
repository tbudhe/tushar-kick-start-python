# 2026-11-02 — two/three-pointer in-place problems, written by Tushar.

# Segregate evens and odds
# NOTE: as written this puts ODDS first. If the task wants EVENS first, see SORTING_NOTES.md.
def segregate_evens_and_odds(numbers):
    l = 0
    r = len(numbers) - 1
    
    while l < r:
        if (numbers[l] % 2 != 0):
            l += 1
        elif (numbers[r] % 2 == 0):
            r -= 1
        else:
            if (numbers[l] % 2 == 0 and numbers[r] % 2 != 0):
                numbers[l], numbers[r] = numbers[r], numbers[l]
                r -= 1
            else:
                l += 1
    return numbers


# Merge One Sorted Array Into Another (same idea as LC 88)
def merge_one_into_another(first, second):
    m = len(first)
    n = len(second)
    
    fi = n - 1         # Points to the very end of second (buffer space)
    ni = m - 1         # Points to the last valid element of second's initial numbers
    mi = m - 1         # Points to the last element of first
    
    # Merge from back to front
    while mi >= 0 and ni >= 0:
        if second[ni] >= first[mi]:
            second[fi] = second[ni]
            ni -= 1
        else:
            second[fi] = first[mi]
            mi -= 1
        fi -= 1
        
    # If any elements are left in first, copy them over
    while mi >= 0:
        second[fi] = first[mi]
        fi -= 1
        mi -= 1
        
    # If any elements are left in second, copy them over (though usually ni reaches 0 first)
    while ni >= 0:
        second[fi] = second[ni]
        fi -= 1
        ni -= 1
        
    return second


# Dutch National Flag (R, G, B)
def dutch_flag_sort(balls): # R,G,B
    ri = 0
    bi = len(balls) - 1
    gi = 0
    while gi <= bi:
        if balls[gi] == 'R':
            balls[ri], balls[gi] = balls[gi], balls[ri]
            ri += 1
            gi += 1
        elif balls[gi] == 'B':
            balls[bi], balls[gi] = balls[gi], balls[bi]
            bi -= 1
        else:
            gi += 1
    return balls


print(segregate_evens_and_odds([1, 2, 3, 4]))
print(merge_one_into_another([1, 3, 5], [2, 4, 6, 0, 0, 0]))
print(dutch_flag_sort(["G", "B", "G", "G", "R", "B", "R", "G"]))
