/**
 * Queue Utilities Example
 * 
 * Demonstrates usage of Queue, Stack, PriorityQueue, Deque, CircularBuffer,
 * and QueueUtils classes.
 */

import { Queue, Stack, PriorityQueue, Deque, CircularBuffer, QueueUtils } from '../queue_utils/mod';

console.log('=== Queue Utilities Examples ===\n');

// ==================== Queue (FIFO) Example ====================
console.log('--- Queue (FIFO) ---');
const printQueue = new Queue<string>();
printQueue.enqueue('Document1.pdf');
printQueue.enqueue('Document2.pdf');
printQueue.enqueue('Document3.pdf');

console.log('Print queue:', printQueue.toArray());
console.log('Next to print:', printQueue.peek());
console.log('Printing:', printQueue.dequeue());
console.log('Remaining:', printQueue.toArray());
console.log();

// ==================== Stack (LIFO) Example ====================
console.log('--- Stack (LIFO) ---');
const browserHistory = new Stack<string>();
browserHistory.push('google.com');
browserHistory.push('github.com');
browserHistory.push('stackoverflow.com');

console.log('History stack:', browserHistory.toArray());
console.log('Current page:', browserHistory.peek());
console.log('Going back to:', browserHistory.pop());
console.log('Remaining history:', browserHistory.toArray());
console.log();

// ==================== Priority Queue Example ====================
console.log('--- Priority Queue ---');
const taskQueue = new PriorityQueue<string>();
taskQueue.enqueue('Low priority task', 1);
taskQueue.enqueue('Critical bug fix', 10);
taskQueue.enqueue('Medium feature', 5);
taskQueue.enqueue('Urgent review', 8);

console.log('Task queue (with priorities):', taskQueue.toArrayWithPriority());
console.log('Next task:', taskQueue.peek(), '(priority:', taskQueue.peekPriority() + ')');
console.log('Processing:', taskQueue.dequeue());
console.log('Processing:', taskQueue.dequeue());
console.log('Remaining:', taskQueue.toArray());
console.log();

// ==================== Deque Example ====================
console.log('--- Deque (Double-ended Queue) ---');
const slideWindow = new Deque<number>();
slideWindow.pushBack(10);
slideWindow.pushBack(20);
slideWindow.pushFront(5);
slideWindow.pushBack(30);

console.log('Window:', slideWindow.toArray());
console.log('Front:', slideWindow.peekFront());
console.log('Back:', slideWindow.peekBack());
console.log('Pop front:', slideWindow.popFront());
console.log('Pop back:', slideWindow.popBack());
console.log('Remaining:', slideWindow.toArray());
console.log();

// ==================== Circular Buffer Example ====================
console.log('--- Circular Buffer ---');
const sensorData = new CircularBuffer<number>(5);
sensorData.write(23.5);
sensorData.write(24.0);
sensorData.write(24.5);
sensorData.write(25.0);
sensorData.write(25.5);
sensorData.write(26.0); // Overwrites 23.5

console.log('Sensor readings (last 5):', sensorData.toArray());
console.log('Oldest reading:', sensorData.peek());
console.log('Buffer full?', sensorData.isFull());
console.log();

// ==================== QueueUtils Examples ====================
console.log('--- QueueUtils ---');

// From array
const numbers = QueueUtils.fromArray([1, 2, 3, 4, 5]);
console.log('From array:', numbers.toArray());

// Reverse
const reversed = QueueUtils.reverse(numbers);
console.log('Reversed:', reversed.toArray());

// Merge
const q1 = QueueUtils.fromArray([1, 2]);
const q2 = QueueUtils.fromArray([3, 4]);
const merged = QueueUtils.merge(q1, q2);
console.log('Merged:', merged.toArray());

// Filter
const evens = QueueUtils.filter(numbers, n => n % 2 === 0);
console.log('Even numbers:', evens.toArray());

// Map
const doubled = QueueUtils.map(numbers, n => n * 2);
console.log('Doubled:', doubled.toArray());

// Reduce
const sum = QueueUtils.reduce(numbers, (acc, n) => acc + n, 0);
console.log('Sum:', sum);

// Find
const firstEven = QueueUtils.find(numbers, n => n % 2 === 0);
console.log('First even:', firstEven);

// Count
const oddCount = QueueUtils.count(numbers, n => n % 2 !== 0);
console.log('Odd count:', oddCount);

// Is palindrome
const palindrome = QueueUtils.fromArray([1, 2, 3, 2, 1]);
const notPalindrome = QueueUtils.fromArray([1, 2, 3, 4, 5]);
console.log('Is [1,2,3,2,1] palindrome?', QueueUtils.isPalindrome(palindrome));
console.log('Is [1,2,3,4,5] palindrome?', QueueUtils.isPalindrome(notPalindrome));
console.log();

// ==================== Real-world Examples ====================
console.log('--- Real-world: BFS Traversal ---');

// Breadth-First Search using Queue
interface Node {
    value: string;
    neighbors: Node[];
}

const nodeA: Node = { value: 'A', neighbors: [] };
const nodeB: Node = { value: 'B', neighbors: [] };
const nodeC: Node = { value: 'C', neighbors: [] };
const nodeD: Node = { value: 'D', neighbors: [] };
const nodeE: Node = { value: 'E', neighbors: [] };

nodeA.neighbors = [nodeB, nodeC];
nodeB.neighbors = [nodeD, nodeE];

function bfs(start: Node): string[] {
    const queue = new Queue<Node>();
    const visited = new Set<string>();
    const result: string[] = [];
    
    queue.enqueue(start);
    visited.add(start.value);
    
    while (!queue.isEmpty()) {
        const current = queue.dequeue()!;
        result.push(current.value);
        
        for (const neighbor of current.neighbors) {
            if (!visited.has(neighbor.value)) {
                visited.add(neighbor.value);
                queue.enqueue(neighbor);
            }
        }
    }
    
    return result;
}

console.log('BFS traversal from A:', bfs(nodeA));
console.log();

// ==================== Real-world: Undo System ====================
console.log('--- Real-world: Undo System ---');

class TextEditor {
    private content: string = '';
    private undoStack = new Stack<string>();
    private redoStack = new Stack<string>();
    
    type(text: string): void {
        this.undoStack.push(this.content);
        this.content += text;
        this.redoStack.clear();
    }
    
    undo(): void {
        if (this.undoStack.isEmpty()) return;
        this.redoStack.push(this.content);
        this.content = this.undoStack.pop()!;
    }
    
    redo(): void {
        if (this.redoStack.isEmpty()) return;
        this.undoStack.push(this.content);
        this.content = this.redoStack.pop()!;
    }
    
    getContent(): string {
        return this.content;
    }
}

const editor = new TextEditor();
editor.type('Hello');
console.log('After typing "Hello":', editor.getContent());
editor.type(' World');
console.log('After typing " World":', editor.getContent());
editor.undo();
console.log('After undo:', editor.getContent());
editor.redo();
console.log('After redo:', editor.getContent());

console.log('\n=== End of Examples ===');
