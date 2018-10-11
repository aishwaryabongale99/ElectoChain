from django.db import models
from auth.models import ActiveVoter
import hashlib
import random
import secrets
import time
import json


class Transaction(models.Model):
    voter_id = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    candidate_hash = models.CharField(max_length=100)

    def createNewTransaction(self, voter_id, candidateId):
        self.voter_id = voter_id
        self.salt = secrets.token_hex(5)
        self.calculateCandidateHash(candidateId)

    def calculateCandidateHash(self, candidateId):
        sha = hashlib.sha256()
        data = candidateId + str(self.salt)
        sha.update(data.encode('utf-8'))
        self.candidate_hash = sha.hexdigest()

    def __str__(self):
        return str(self.voter_id) + '--' + str(self.candidate_hash)


class Block(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    prev_hash = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)

    def __str__(self):
        return str(self.hash)

    def createNewBlock(self, transaction, prevBlock):
        self.transaction = transaction
        self.prev_hash = prevBlock.hash
        self.nonce = 0
        self.difficulty = 5
        self.mineBlock()
        return self

    def generateHash(self):
        sha = hashlib.sha256()
        data = str(self.timestamp) + self.prev_hash + str(self.transaction)
        sha.update(data.encode('utf-8'))
        return hash

    def mineBlock(self):
        target = str('0' * self.difficulty)
        while str(self.hash)[:self.difficulty] != target:
            self.nonce = self.nonce + 1
            self.hash = self.generateHash()


class Peer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name + "@" + self.address

    def createNewPeer(self, name, address):
        self.name = name
        self.address = address
        return self


class Check(models.Model):
    port = models.CharField(max_length=50)

    def __str__(self):
        return self.port



