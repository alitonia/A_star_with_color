# A_star_with_color
Search for a path to destination in graph, granted being at a node give distance to all neighbor nodes.

This program assumes predicted cost is the same as distance.


### Extending capacity:

* Remove the `harper` part in main to use directed graph.

* Change `get_neighbor_nodes` to extend to arbitrary geometric shape (ex: weight-less graph,  tranverse in hexagon, ....).


### Possible improvements:

* Implement of `PriorityNodeQueue` is inefficient.

* Class Alpha prints `Alpha.a` instead of `A`.
