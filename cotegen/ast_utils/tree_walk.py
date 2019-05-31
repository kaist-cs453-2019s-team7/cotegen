import astor

class TreeWalk(astor.TreeWalk):
  def replace(self, new_node):
        """Replace a node after first checking integrity of node stack."""
        cur_node = self.cur_node
        nodestack = self.nodestack
        cur = nodestack[-1]
        prev = nodestack[-2]
        index = prev[-1] - 1
        oldnode, name = prev[-2][index]
        assert cur[0] is cur_node, (cur[0], cur_node)
        assert cur_node is oldnode, (cur_node, prev[-2], index)
        parent = prev[0]

        if isinstance(parent, list):
            parent[index] = new_node
        else:
            setattr(parent, name, new_node)
