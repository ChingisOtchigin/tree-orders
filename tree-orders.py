import random
import argparse
from PIL import Image, ImageDraw, ImageFont
import math

class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self, max_size = 5):
        self.img = Image.new('RGBA', (800, 500), color = (250, 250, 250))
        self.font = ImageFont.truetype('arial.ttf', 20)

        max_size = min(max_size, 5)
        self.levels = 0
        q = []
        self.root = self.generate_node(self.levels, q)
        while not len(q) == 0:
            current, level = q.pop(0)
            if level < max_size:
                current.left = self.generate_node(level, q)
                current.right = self.generate_node(level, q)
    
    def generate_node(self, level, q):
        if random.random() < (1 - 0.2 * level):
            node = Node(random.randint(1,9))
            q.append((node, level + 1))
            self.levels = max(self.levels, level + 1)
            return node
        else:
            return None


    def draw_tree(self, node, coordinates, level):
        if node is None:
            return

        d = ImageDraw.Draw(self.img)
        d.ellipse((coordinates[0], coordinates[1], coordinates[0]+50, coordinates[1]+50), fill=(255, 0, 0, 0), outline=(0, 0, 0))
        d.text((coordinates[0]+15,coordinates[1]+15), node.data, font=self.font, fill=(0,0,0))

        next_level_spacing = (500 - (2**(level+1))*50) // (2**(level+1) + 1)
        if node.left:
            next_x = coordinates[0] - ((next_level_spacing//2) + 25)
            next_y = coordinates[1] + 100
            d.line((coordinates[0] + 25 - math.cos(math.pi/12), 200, next_x + 25, next_y), fill=(0, 0, 0), width=10)
    
    def to_list(self, node):
        if node is None:
            return None
        return [node.data, self.to_list(node.left), self.to_list(node.right)]
    
    def __str__(self):
        return str(self.to_list(self.root))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", help="Number of trees to generate. Default 10. Minimum 1. Maximum 50")
    args = parser.parse_args()
    num_trees = 10
    if args.number:
        num_trees = max(min(int(args.number), 50), 1)
    
    trees = [BinaryTree() for i in range(num_trees)]
    for i, tree in enumerate(trees):
        print(tree)
        tree.img.save(f'questions/q{i}.png')