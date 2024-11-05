def organize_into_groups(numbers:list, group_size:int, target_avg:float, tolerance=0.1):
    """
    Organize a list of numbers into groups that have averages close to the target.
    
    Parameters:
    numbers (list): List of numbers to organize
    group_size (int): Size of each group
    target_avg (float): Desired average for each group
    tolerance (float): Acceptable deviation from target average
    
    Returns:
    list: List of groups that satisfy the conditions
    """
    # Make a copy to avoid modifying original list
    remaining_numbers = numbers.copy()
    groups = []
    
    while len(remaining_numbers) >= group_size:
        # Sort remaining numbers to help with selection
        remaining_numbers.sort()
        
        # Initialize current group
        current_group = []
        target_sum = target_avg * group_size
        
        # Try to find numbers that sum close to target
        current_sum = 0
        
        # Start with middle numbers to get closer to target average
        while len(current_group) < group_size:
            best_number = None
            best_diff = float('inf')
            
            # Find the number that gets us closest to target
            for num in remaining_numbers:
                if num in current_group:
                    continue
                    
                temp_sum = current_sum + num
                temp_avg = temp_sum / (len(current_group) + 1)
                needed_avg = (target_sum - temp_sum) / (group_size - len(current_group) - 1) if len(current_group) < group_size - 1 else temp_avg
                
                if 1 <= needed_avg <= 5:  # Check if remaining numbers could achieve target
                    diff = abs(temp_avg - target_avg)
                    if diff < best_diff:
                        best_diff = diff
                        best_number = num
            
            if best_number is None:
                break
                
            current_group.append(best_number)
            remaining_numbers.remove(best_number)
            current_sum = sum(current_group)
        
        if len(current_group) == group_size:
            group_avg = sum(current_group) / group_size
            if abs(group_avg - target_avg) <= tolerance:
                groups.append(current_group)
            else:
                # If we couldn't make a good group, put numbers back
                remaining_numbers.extend(current_group)
        else:
            # If we couldn't complete a group, put numbers back
            remaining_numbers.extend(current_group)
            break
            
    return groups, remaining_numbers

# Example usage
numbers = [1.2, 2.3, 3.1, 4.2, 5.0, 2.8, 3.7, 4.1, 1.5, 2.9, 3.8, 4.5, 2.1, 3.3, 4.7]
group_size = 5
target_average = 3.5

groups, leftover = organize_into_groups(numbers, group_size, target_average)

print("Original numbers:", numbers)
print("\nGroups formed:")
for i, group in enumerate(groups, 1):
    print(f"Group {i}: {group} (average: {sum(group)/len(group):.2f})")
if leftover:
    print("\nLeftover numbers:", leftover)