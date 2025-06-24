from __future__ import annotations
import logging

from utils.configure_logger import ConfigureLogger
from utils.timed_audio import TimedAudio
from entry import Entry, AudioMetadata

# retrieve class logger and configure logger
logger = logging.getLogger(__name__)
join_voice_channel_logger_config = ConfigureLogger(logger=logger)

# create child class of Entry for the linked list
class AudioQueueEntry(Entry):
    __slots__ = ('next',)

    def __init__(self, audio_metadata:tuple=None, message_information:tuple=None, timed_audio:TimedAudio=None, next:AudioQueueEntry=None):
        super().__init__(audio_metadata, message_information, timed_audio)
        self.next = next
        logger.info(f'Creating AudioQueueEntry with audio metadata: {audio_metadata}\n, message information: {message_information}\n, and next: {next}')
    
    def set_next(self, next:AudioQueueEntry=None):
        self.next = next
        logger.info(f'Setting next: {next}')
    
# linked list queue implementation
class AudioQueueLinkedList():
    def __init__(self):
        self.size = 0
        self.tail = AudioQueueEntry(None, None, None)
        self.head = AudioQueueEntry(None, None, self.tail)
        self.curr_entry = self.head

    def enqueue(self, audio_metadata:tuple, message_information:tuple, timed_audio:TimedAudio):
        logger.info(f'Enqueue requested')
        if not audio_metadata or not message_information or not timed_audio:
            return

        entry = AudioQueueEntry(audio_metadata, message_information, timed_audio, self.tail)
        self.curr_entry.set_next(entry)
        self.curr_entry = entry
        self.size += 1
        logger.info(f'Enqueuing AudioQueueEntry with metadata: {entry.audio_metadata}\n and message information: {entry.message_information}')
        logger.info(f'Queue:\n{self.get_printable()}')
    
    def dequeue(self) -> Entry:
        logger.info(f'Dequeue requested')
        if self.curr_entry == self.head:
            logger.info(f'No entries to dequeue')
            return None

        entry = self.head.next
        if self.curr_entry == entry:
            self.curr_entry = self.head
            logger.info(f'Dequeuing last entry')

        self.head.set_next(entry.next)
        self.size -= 1
        logger.info(f'Dequeuing AudioQueueEntry with metadata: {entry.audio_metadata}\n and message information: {entry.message_information}')
        logger.info(f'Queue:\n{self.get_printable()}')
        return entry
    
    def find_entry(self, idx:int=1) -> Entry:
        logger.info(f'Find entry requested')
        if idx < 1 or idx > self.size - 1:
            logger.info(f'Entry out of range')
            return None
                
        entry = self.head
        for _ in range(idx):
            entry = entry.next

        return entry
        
    def remove(self, idx:int=1) -> Entry:
        logger.info(f'Remove requested with index {idx}')
        if idx < 1 or idx > self.size - 1:
            logger.info(f'Entry out of range')
            return None

        if idx == 1:
            return self.dequeue()

        previous_entry = self.find_entry(idx - 1)
        entry = previous_entry.next
        
        previous_entry.next = entry.next
        self.size -= 1

        logger.info(f'Removing AudioQueueEntry with metadata: {entry.audio_metadata}\n and message information: {entry.message_information}')
        logger.info(f'Queue:\n{self.get_printable()}')
        return entry
    
    def is_empty(self) -> bool:
        return (self.size == 0)

    def get_printable(self) -> str:
        logger.info(f'Get printable requested')
        printable = f''
        if self.size == 0:
            return printable

        curr_entry = self.head.next
        cnt = 1
        for _ in range(self.size - 1):
            printable += f'{cnt}. {curr_entry.audio_metadata[AudioMetadata.TITLE.value]}\n'
            cnt += 1
            curr_entry = curr_entry.next
        printable += f'{cnt}. {curr_entry.audio_metadata[AudioMetadata.TITLE.value]}\n'
        return printable