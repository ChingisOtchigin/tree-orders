import random
import argparse
from PIL import Image, ImageDraw, ImageFont
import math
from os import mkdir, path, getcwd

class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self, max_size = 5):
        self.img = Image.new('RGBA', (2048, 512), color = (250, 250, 250))
        self.font = ImageFont.truetype('arial.ttf', 20)

        self.max_size = min(max_size, 5)
        self.leaning = random.randint(0,2) #left, mid, right

        self.root = Node(random.randint(0,99))

        self.levels = self.generate_tree(self.root)
        # q = []
        # self.root = self.generate_node(self.levels, q)
        # while not len(q) == 0:
        #     current, level = q.pop(0)
        #     if level < max_size:
        #         current.left = self.generate_node(level, q)
        #         current.right = self.generate_node(level, q)
    
    def generate_tree(self, node, level=0):
        chance_left = chance_right = 1 - 0.2 * level
        chance_left += [0.2, 0, -0.2][self.leaning]
        chance_right += [-0.2, 0, 0.2][self.leaning]
        max_level_left = max_level_right = level

        if level+1 < self.max_size:
            if random.random() < chance_left:
                node.left = Node(random.randint(0,99))
                max_level_left = self.generate_tree(node.left, level + 1)
            
            if random.random() < chance_right:
                node.right = Node(random.randint(0,99))
                max_level_right = self.generate_tree(node.right, level + 1)

        return max(max_level_left, max_level_right)

    def generate_node(self, level, q):
        if random.random() < (1 - 0.2 * level):
            node = Node(random.randint(1,9))
            q.append((node, level + 1))
            self.levels = max(self.levels, level + 1)
            return node
        else:
            return None


    def draw_tree(self, node, coordinates=(999,50), level=0):
        if node is None:
            return

        d = ImageDraw.Draw(self.img)
        d.ellipse((coordinates[0], coordinates[1], coordinates[0]+50, coordinates[1]+50), fill=(255, 0, 0, 0), outline=(0, 0, 0))
        
        text_string = str(node.data)
        text_location = (coordinates[0]+15,coordinates[1]+15) if len(text_string) == 2 else (coordinates[0]+20,coordinates[1]+20)

        d.text(text_location, text_string, font=self.font, fill=(0,0,0))

        next_level_spacing = (2048 - (2**(level+1))*50) // (2**(level+1) + 1)
        if node.left:
            next_x = coordinates[0] - ((next_level_spacing//2) + 25)
            next_y = coordinates[1] + 100
            d.line((coordinates[0] + 25 - 25*math.cos(math.pi/12), coordinates[1] + 25 + 25*math.sin(math.pi/12), next_x + 25, next_y), fill=(0, 0, 0), width=3)
            self.draw_tree(node.left, (next_x, next_y), level+1)
        if node.right:
            next_x = coordinates[0] + ((next_level_spacing//2) + 25)
            next_y = coordinates[1] + 100
            d.line((coordinates[0] + 25 + 25*math.cos(math.pi/12), coordinates[1] + 25 + 25*math.sin(math.pi/12), next_x + 25, next_y), fill=(0, 0, 0), width=3)
            self.draw_tree(node.right, (next_x, next_y), level+1)
    
    def to_list(self, node):
        if node is None:
            return None
        return [node.data, self.to_list(node.left), self.to_list(node.right)]
    
    def preorder(self, node):
        if node is None:
            return []
        return [node.data] + self.preorder(node.left) + self.preorder(node.right)

    def inorder(self, node):
        if node is None:
            return []
        return self.inorder(node.left) + [node.data] + self.inorder(node.right)
    
    def postorder(self, node):
        if node is None:
            return []
        return  self.postorder(node.left) + self.postorder(node.right) + [node.data]
    
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

    mydir = path.join(getcwd(), f'questions')
    if not path.isdir(mydir):
        mkdir(mydir)

    file = open('answers.txt', 'w')                                                                                                               
    for i, tree in enumerate(trees):
        print(f'===={i+1}====\n{tree}\n\n')
        tree.draw_tree(tree.root)
        tree.img.save(f'questions/q{i+1}.png')
        file.write(f'===Q{i+1}===\nPreorder: {tree.preorder(tree.root)}\nInorder: {tree.inorder(tree.root)}\nPostorder: {tree.postorder(tree.root)}\n\n')                                                      