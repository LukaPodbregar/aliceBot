# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

#(interaction_data) Data of an interaction
class CAInteractionData(models.Model):
	userID = models.CharField(max_length=100) #User ID = agentID
	screenID = models.CharField(max_length=100) #Screen where the conversation takes place
	userM = models.CharField(max_length=255) #User message
	caM = models.CharField(max_length=255) #CA message (agentMessage)
	caPreMood = models.IntegerField() #CA mood before sending message (agentPreMood)
	caPreEmotion = models.IntegerField() #CA emotion before sending message (agentPreEmotion)
	caNeed = models.BooleanField() #CA need state (0 NOT need, 1 need)
	caAction = models.CharField(max_length=255) #CA action in Unity
	processTime = models.FloatField() #Time to calculate caM
	timestamp = models.CharField(max_length=100)

#(training_data) Data stored everytime some processing is done
class TrainingData(models.Model):
	userID = models.CharField(max_length=100) #User ID = agentID
	userM = models.CharField(max_length=255) #User message analyzed (userMessage)
	analysisType = models.CharField(max_length=100) #Type of analysis performed
	assignedTag = models.CharField(max_length=100) #Assigned tag after analysis
	detectedKeys = models.CharField(max_length=100) #Keywords detected during analysis
	innerTaskID = models.CharField(max_length=100) #To know from what task is the message (dialogID)
	innerStateID = models.CharField(max_length=100) #To know in what state the message was generated (stateID)
	processTime = models.FloatField() #Time to analyze input
	timestamp = models.CharField(max_length=100)
	
#(device_interaction_data) Data stored everytime a button is clicked
class DeviceInteractionData(models.Model):
	userID = models.CharField(max_length=100) #User ID
	screenID = models.CharField(max_length=100) #Screen ID
	type = models.CharField(max_length=100) #Type
	buttonID = models.CharField(max_length=100) #Button ID
	xPos = models.CharField(max_length=100) #x position
	yPos = models.CharField(max_length=100) #y position
	timestamp = models.CharField(max_length=100)

#(points_record_data) Points Record Data
class PointsRecordData(models.Model):
	userID = models.CharField(max_length=100) #User ID
	points = models.FloatField() #Current points of the user
	pointsToAdd = models.FloatField() #Current pointsToAdd of the user
	screenID = models.CharField(max_length=100) #Screen where the update has been checked
	timestamp = models.CharField(max_length=100)
	
#(classification_data) Data stored everytime a classification is performed
class ClassificationData(models.Model):
	message = models.CharField(max_length=255) #User message
	processedWords = models.CharField(max_length=255) #Processed words
	classificationType = models.CharField(max_length=100) #Type of classification performed
	MLprobabilities = models.CharField(max_length=255) #Probabilities of classes
	classResult = models.CharField(max_length=100) #Assigned tag after classification
	processTime = models.FloatField() #Time to analyze input
	timestamp = models.CharField(max_length=100)
	

#(seca_answer) Class with the bot answer that is sent to Unity
class CAAnswer(models.Model):
    response = models.CharField(max_length=100) #message
    #Mood information to update the Earth state
    mood = models.IntegerField() #mood
    emotion = models.IntegerField() #emotion
    #0/1 Integer to know if Conversation finished
    end = models.IntegerField() #end
    #Extra tag to detect special information in Unity
    tag = models.CharField(max_length=100) #tag


#(seca_attention_need) Class to know if the CA needs
class CANeed(models.Model):
	need = models.BooleanField() #state


#(memory) Single Memory Data
class CAMemory(models.Model):
	memoryID = models.CharField(max_length=100) #agentID
	memory = models.CharField(max_length=100) #memoryID
	counter = models.IntegerField() #counter
	category = models.CharField(max_length=100) #category


#(personality_state) CA State (used to reload the agent if the server falls)
class CAState(models.Model):
	agentID = models.CharField(max_length=100) #agentID
	mood = models.IntegerField() #currentMood
	emotion = models.IntegerField() #currentEmotion


#(empathy_component) Single Empathy Component Data
class CAEmpathyC(models.Model):
	empathyID = models.CharField(max_length=100) #agentID
	component = models.CharField(max_length=100) #componentID
	value = models.FloatField() #value
	maxVal = models.FloatField() #maxValue


#(seca_empathy_value) Empathy Component Value Data
class CAEmpathyCV(models.Model):
	value = models.FloatField()