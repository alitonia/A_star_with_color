import collections
from typing import Dict, List, Union, Any

from colorama import Style, init, Fore, deinit


class Node:
	def __init__(self, name: Any, distance: int, history: list):
		self.name = name
		self.distance = distance
		self.history = history
	
	def __repr__(self):
		return f'{Fore.GREEN}Node{Style.RESET_ALL}' \
		       f'(name: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL}, distance: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL})' \
		       % (self.name, self.distance)
	
	def __str__(self):
		return f'{Fore.GREEN}Node{Style.RESET_ALL}' \
		       f'(name: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL}, distance: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL})' \
		       % (self.name, self.distance)


class Blob:
	def __init__(self, priority: int, *args):
		self.priority = priority
		
		if len(args) == 1:
			self.node = args[0]
		elif len(args) == 3:
			self.node = Node(*args)
	
	def __repr__(self):
		return f'{Fore.GREEN}Blob{Style.RESET_ALL}' \
		       f'(prior: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL}, {Fore.LIGHTRED_EX}%s{Style.RESET_ALL})' \
		       % (self.priority, str(self.node))
	
	def __str__(self):
		return f'{Fore.GREEN}Blob{Style.RESET_ALL}' \
		       f'(prior: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL}, {Fore.LIGHTRED_EX}%s{Style.RESET_ALL})' \
		       % (self.priority, str(self.node))


class PriorityNodeQueue:
	
	def __init__(self, *iterable: Blob):
		# pass in list of tuple (priority, data)
		self.holder: List[Blob] = list(sorted(iterable, key=lambda b: b.priority))
		self.check_membership_data: List[Node] = [b.node for b in self.holder]
	
	def __str__(self):
		return f'[%s]' % ', '.join(
			f'{Fore.GREEN}Blob{Style.RESET_ALL}'
			f'(prior: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL}, name: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL})'
			% (b.priority, b.node.name) for b in self.holder)
	
	def __len__(self):
		return len(self.holder)
	
	def is_empty(self):
		return len(self.holder) == 0
	
	def clear(self):
		self.holder = []
		self.check_membership_data = []
	
	def pop(self) -> Union[Node, None]:
		if self.is_empty():
			return None
		else:
			return_node = self.holder.pop(0).node
			self.check_membership_data.remove(return_node)
			return return_node
	
	def show(self):
		return self.holder
	
	def get_node_length(self, node_name: Any) -> int:
		"""
		
		:param node_name:
		:return: -1 if not found, else weight of node
		"""
		for node in self.check_membership_data:
			if node.name == node_name:
				return node.distance
		return -1
	
	def push(self, blob: Blob) -> int:
		node_distance_if_existed = self.get_node_length(blob.node.name)
		
		if node_distance_if_existed == -1:
			i = 0
			while i < len(self.holder) and self.holder[i].priority < blob.priority:
				i += 1
			self.holder.insert(i, blob)
			self.check_membership_data.append(blob.node)
		else:
			if node_distance_if_existed <= blob.node.distance:
				return -1
			
			index_of_holder_removal = []
			index_of_data_removal = []
			for i in range(len(self.holder)):
				if self.holder[i].node.name == blob.node.name:
					index_of_holder_removal.append(i)
				if self.check_membership_data[i].name == blob.node.name:
					index_of_data_removal.append(i)
			
			for index in reversed(index_of_holder_removal):
				del self.holder[index]
			for index in reversed(index_of_data_removal):
				del self.check_membership_data[index]
		self.push(blob)
		return 0


def get_neighbor_nodes(visiting_node, blue_graph: Dict[Any, List[Node]]) -> List[Node]:
	return blue_graph.get(visiting_node) or []


def solve(magic_graph: Dict[Any, List[Node]], starting_point: Any, ending_node: Any) -> int:
	visited = dict()
	fridge = PriorityNodeQueue()
	
	fridge.push(Blob(0, starting_point, 0, []))
	
	while not fridge.is_empty():
		target_node = fridge.pop()
		visiting_node, current_distance, history_a = target_node.name, target_node.distance, target_node.history
		
		print(
			f'Visiting node {Fore.LIGHTRED_EX}%s{Style.RESET_ALL},'
			f' distance from start: {Fore.LIGHTRED_EX}%s{Style.RESET_ALL}'
			% (visiting_node, current_distance))
		
		visited[visiting_node] = (
			current_distance
			if (not visited.get(visiting_node) or visited.get(visiting_node) > current_distance)
			else visited.get(visiting_node))
		
		if visiting_node == ending_node:
			print(f'{Fore.LIGHTYELLOW_EX}This is the ending node.')
			print(f'{Fore.LIGHTYELLOW_EX}Path taken: %s' % (history_a + [visiting_node]))
			return 0
		else:
			print(f'This is not ending node. Getting neighbors....')
			neighbor_nodes = [Node(node.name, node.distance + current_distance, history_a + [visiting_node]) for node
			                  in
			                  get_neighbor_nodes(visiting_node, magic_graph)
			                  ]
			print(f'{Fore.YELLOW}Neighbors:{Style.RESET_ALL} %s' % neighbor_nodes)
			
			# only neighbor not visited, or visited with weight greater than now is used
			valid_neighbor_nodes = []
			for node in neighbor_nodes:
				historical_distance_if_exist = visited.get(node.name)
				node_distance_in_fridge_if_exist = fridge.get_node_length(node.name)
				
				history_approved = (
						(historical_distance_if_exist is None)
						or (historical_distance_if_exist > node.distance)
				)
				
				fridge_approved = (
						(node_distance_in_fridge_if_exist == -1)
						or (node_distance_in_fridge_if_exist > node.distance)
				)
				if history_approved and fridge_approved:
					valid_neighbor_nodes.append(node)
					if historical_distance_if_exist:
						visited[node.name] = node.distance
			
			print(f'{Fore.YELLOW}Valid neighbors:{Style.RESET_ALL} %s' % valid_neighbor_nodes)
			
			for node in valid_neighbor_nodes:
				fridge.push(Blob(node.distance, node))
			
			print(f'{Fore.YELLOW}Visited:{Style.RESET_ALL} %s' % visited.keys())
			print(f'{Fore.YELLOW}Fridge:{Style.RESET_ALL} %s' % fridge)
			
			print('-' * 10)
	return -1


if __name__ == '__main__':
	init(autoreset=True)
	rainbow_graph = {
		'A': [('B', 5), ('C', 7), ('D', 9)],
		'B': [('G', 6), ('E', 4), ('C', 3)],
		'C': [('E', 2)],
		'E': [('G', 4), ('H', 4)],
		'G': [('K', 5)],
		'K': [('H', 5)],
		'H': [('F', 2)],
		'F': [('D', 2)],
		'D': [('A', 9)],
	}
	
	# Extension: a predictive table of estimate cost to get to a node.
	# Simulate by adding cost to all edges of node
	manual_labor = {
		'A': 1,
		'B': 1,
		'C': 1,
		'D': 1,
		'E': 1,
		'F': 1,
		'G': 1,
		'H': 1,
		'K': 1
	}
	unsuspected_hill = collections.defaultdict(lambda: 0)
	for (key, value) in manual_labor.items():
		unsuspected_hill[key] = value
	
	# This part turn directed graph to non-directed one
	harper = []
	# get all pairs
	for (key, things) in rainbow_graph.items():
		for thing in things:
			harper.append(tuple((key, thing[0], thing[1]))
			              if key > thing[0] else tuple((thing[0], key, thing[1]))
			              )
	
	# remove duplicate
	harper = list(sorted(set(harper)))
	
	rainbow_keys = sorted([key for key in rainbow_graph.keys()])
	rainbow_graph = dict()
	
	for key in rainbow_keys:
		rainbow_graph[key] = [[x for x in list(thing) if x != key] for thing in harper if key in thing]
	
	print('Data: ')
	for thing in rainbow_graph.items():
		print(thing)
	print('-' * 20)
	rainbow_graph = {start_node: [Node(*node_data, []) for node_data in neighbor_list]
	                 for (start_node, neighbor_list) in rainbow_graph.items()}
	
	solve(rainbow_graph, 'A', 'K')
	deinit()
