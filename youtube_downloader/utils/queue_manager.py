import os
import json

class QueueManager:
    def __init__(self, queue_file="download_queue.json"):
        self.queue_file = queue_file
        self.download_queue = self.load_queue()

    def load_queue(self):
        """Load the download queue from file"""
        try:
            if os.path.exists(self.queue_file):
                with open(self.queue_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading queue: {e}")
            return []

    def save_queue(self, queue):
        """Save the download queue to file"""
        try:
            with open(self.queue_file, 'w') as f:
                json.dump(queue, f)
        except Exception as e:
            print(f"Error saving queue: {e}")

    def get_queue(self):
        """Get the current queue"""
        return self.download_queue

    def update_queue(self, urls):
        """Update the queue with new URLs"""
        self.download_queue = [url for url in urls if url.strip()]
        self.save_queue(self.download_queue)

    def clear_queue(self):
        """Clear the queue and save"""
        self.download_queue = []
        self.save_queue(self.download_queue) 