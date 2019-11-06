"""
Given a building with 'n' number of floors, 'l' number of elevators. Each lift is assumed to contain infinite capacity.

If a floor has people waiting for a lift, the input data for that floor will be of the form
[fi, p, f1, f2, f3, .......fp] where fi is the floor number, p is the number of people waiting at that floor and
f1 -> fp are the target floors they want to reach.

Once a person gets into a lift, he will only get down if he reaches his target floor. We assume that all our lifts are
waiting at floor 0 initially.

The complete input data is a list of lists where each element of the outer list is the floor data of a
particular floor as mentioned previously
Example : [[fa, p1, f1,.....fp1], [fb, p2, f1,.....fp2], ........]

How do we get everyone to their destinations while using minimum amount of electricity? Assuming that it takes constant
amount of electricity k, for a lift to move 1 floor (up or down)
"""


# n -> no of floors
# l -> no of elevators
# data -> data of people waiting for lifts
# k -> energy consumed by a lift to move 1 floor
def min_energy(n, l, data, k):

    # up_data contains the data of people going to floors above at each floor
    # up_data = [[f1, f2, f3, .....fn], ......] where f1 is the current floor and f2, f3, ...fn > f1
    # We remove the number of people statistic as it is not necessary
    up_data = [([floor_data[0]] + [floor for floor in floor_data[2:] if floor > floor_data[0]])
               for floor_data in data]

    # In similar fashion, we create down_data for people going down at each floor. For down_data, we also sort the
    # target floor numbers for each floor i.e... for floor_data in down_data, floor_data[0] contains the current floor
    # and target floors i.e.. floor_data[1:] are sorted in an ascending order
    down_data = [([floor_data[0]] + sorted([floor for floor in floor_data[2:] if floor < floor_data[0]]))
                 for floor_data in data]

    # We further sort down_data by the current floor values i.e.. floor_data[0] in a descending order
    down_data.sort(key=lambda x: x[0], reverse=True)

    # First we serve all the up requests i.e.. people waiting to go to floors above their current floors. Since, it
    # is assumed that the lifts have infinite capacity, all up requests can be served with a single lift.
    # This first lift will reach a maximum point (max_point) of all the current floors and destinations
    # of all up requests at which it completes all up requests.
    #
    # Energy spent would be max_point*k
    max_point = max(max(floor_data) for floor_data in up_data)
    energy = max_point*k
    top = max_point
    lifts_used = 1

    # Now we have 1 lift at the top and (l-1) lifts at the bottom waiting to serve the down requests.
    # We will bring in new lifts only when overall energy spent is less than when it is served with top lift.
    # We start with the top most 'current floor' in the down_data and see if it can be served better with
    # the top lift or a new lift. The top lift is used in two scenarios,
    # 1. if current_floor >= top/2 or
    # 2. there are no more lifts available at floor 0
    # The minimum of lowest destination floor of the 'current floor' and 'top' becomes the new 'top'.
    # If any of the above 2 scenarios are not met, we bring a new lift from floor 0 and
    # serve the requests for the 'current floor', It's lowest destination becomes the new 'top'
    # we move to next floor_data in down_data and serve further requests using this new lift and remaining lifts at bottom

    for floor_data in down_data:
        if floor_data[0] >= top/2.0 or lifts_used == l:
            lowest_dest = min(floor_data[1], top)
            energy += (top-lowest_dest)*k
            top = lowest_dest
        else:
            lowest_dest = floor_data[1]
            energy += (2*floor_data[0]-floor_data[1])*k  # floor_data[0] + (floor_data[0] - floor_data[1])
            top = lowest_dest
            lifts_used += 1

    return energy, lifts_used
