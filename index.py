
# -*- coding: utf-8 -*-

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

import logging
import json
import six
import boto3

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
lambda_client = boto3.client("lambda")
				
MIN_FAN_SPEED = 1
MAX_FAN_SPEED = 5

class LaunchRequestHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return is_request_type("LaunchRequest")(handler_input)

	def handle(self, handler_input):
		speechText = "Dime que quieres hacer, encender, apagar,establecer temperatura o velocidad del ventilador, o di ayuda"
		rePrompt = "Dime que quieres hacer con el aire acondicionado, ó pide ayuda"

		return handler_input.response_builder.speak(speechText).ask(rePrompt).set_should_end_session(False).response


class HelpIntentHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return is_intent_name("AMAZON.HelpIntent")(handler_input)

	def handle(self, handler_input):
		speechText = "Bienvenidos a la ayuda de Control de aire acondicionado!. Puedes decir cosas como:\
			         dime la temperatura, ó \
					 enciende el aire acondicionado, ó \
				     apaga el aire acondicionado, ó \
					 pon el aire acondicionado a n grados, ó, \
					 pon el ventilador al 2, (entre 1 y 5)"

		return handler_input.response_builder.speak(speechText).response

class CancelAndStopIntentHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return (is_intent_name("AMAZON.CancelIntent")(handler_input) or 
				is_intent_name("AMAZON.StopIntent")(handler_input))
	
	def handle(self, handler_input):
		speechText = "Hasta luego familia!."

		return handler_input.response_builder.speak(speechText).response

class SessionEndedRequestHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return is_request_type("SessionEndedRequest")(handler_input)
	
	def handle(self, handler_input):
		handler_input.response_builder.response

class AllExceptionsHandler(AbstractExceptionHandler):
	def can_handle(self, handler_input, exception):
		return True
	
	def handle(self, handler_input, exception):
		logger.error(exception, exc_info=True)
		speechText = "Lo siento, no he comprendido lo que me has dicho. Di, ayuda, para obtener más información sobre cómo establecer el aire acondicionado."

		return handler_input.response_builder.speak(speechText).response

class ListItemsIntent(AbstractRequestHandler):
	def can_handle(self, handler_input):
		logger.info("Lets see... ******")
		return (is_intent_name("SetTemp")(handler_input) or
                is_intent_name("SwitchOnAC")(handler_input) or
				is_intent_name("SwitchOffAC")(handler_input))
	def handle(self, handler_input):
		speechText = "Lo siento, no me he enterado de nada"		
		logger.info("Evaluating ******")
		slots = handler_input.request_envelope.request.intent.slots
		intentname = handler_input.request_envelope.request.intent.name
		print('intentname:' + intentname)
		setOnOff = ""
		if intentname == "SwitchOnAC" or intentname == "SwitchOffAC" :
			if intentname == "SwitchOnAC":
				setOnOff= "SET_ON"
				speechText = "Vale, enciendo el aire acondicionado"		
			else:
				setOnOff= "SET_OFF"
				speechText = "Vale, apago el aire acondicionado"		
		body = {'StructureName': 'Parlament 36',
					'DeviceName': 'Salon',
					'Action': setOnOff
		}
		logger.info("Calling lambda MELGet ")
		logger.info("With body:" + json.dumps(body))
		response = lambda_client.invoke(
										FunctionName='MELGet',
										InvocationType='RequestResponse',
										Payload=json.dumps(body)
										)			
		if intentname == "SetTemp" or intentname == "SetTempInc":
			defaultTempTarget = None
			for slotName, currentSlot in six.iteritems(slots):
				if slotName == 'tempTarget':
					logger.info("Evaluating slotName "+slotName)
					logger.info("Evaluating currentSlot "+currentSlot.value)
					if currentSlot.value:
						tempTarget = int(currentSlot.value)	
						if intentname == "SetTemp" : 
							Action = 'SET_ON_AT'
						if intentname == "SetTempInc" : 
							Action = 'SET_ON_inc'
						logger.info(tempTarget)
						body =    { 'StructureName': 'Parlament 36',
								'DeviceName': 'Salon',
								'Action': Action ,
								'Temperature': tempTarget
								}
						logger.info("Calling lambda MELGet ")
						logger.info("With body:" + json.dumps(body))
						response = lambda_client.invoke(
									FunctionName='MELGet',
									InvocationType='RequestResponse',
									Payload=json.dumps(body)
						)
						speechText = "<say-as interpret-as=\"interjection\">Perfecto!</say-as>La temperatura se ha establecido a: {0}. <say-as interpret-as=\"interjection\">Salut!</say-as>.".format(tempTarget)
					else:
						speechText = "Lo siento, no he podido entender la cifra de temperatura"		
						logger.info(speechText)
		return handler_input.response_builder.speak(speechText).response

class ListItemsIntentFan(AbstractRequestHandler):
	def can_handle(self, handler_input):
		logger.info("Lets see... ******")
		return (is_intent_name("SetFanSpeed")(handler_input))
	def handle(self, handler_input):
		speechText = "Lo siento, no me he enterado de nada"	
		logger.info("Evaluating ******")
		intentname = handler_input.request_envelope.request.intent.name
		print('intentname:' + intentname)
		slots = handler_input.request_envelope.request.intent.slots
		
		for slotName, currentSlot in six.iteritems(slots):
			if slotName == 'fanSpeedTarget':
				logger.info("Evaluating slotName "+slotName)
				logger.info("Evaluating currentSlot "+currentSlot.value)
				if currentSlot.value:
					fanSpeed = int(currentSlot.value)
					if (fanSpeed>= MIN_FAN_SPEED and fanSpeed <= MAX_FAN_SPEED):
						logger.info(fanSpeed)
						body =  { 'StructureName': 'Parlament 36',
									'DeviceName': 'Salon',
									'Action': 'SET_FAN',
									'FanSpeed': fanSpeed
						}
						logger.info("Calling lambda MELGet ")
						logger.info("With body:" + json.dumps(body))
						response = lambda_client.invoke(
									FunctionName='MELGet',
									InvocationType='RequestResponse',
									Payload=json.dumps(body)
						)
						speechText = "<say-as interpret-as=\"interjection\">Perfecto!</say-as>La velocidad del ventilador se ha establecido a: {0}. <say-as interpret-as=\"interjection\">Salut!</say-as>.".format(fanSpeed)
					else: 
						speechText = "Lo siento, no he podido entender la velocidad del ventilador, el valor tiene que estar entre 1 y 5"		
				else:
					speechText = "Lo siento, no he podido entender la velocidad del ventilador"		
					logger.info(speechText)
		return handler_input.response_builder.speak(speechText).response

class ListItemsIntentGetInfo(AbstractRequestHandler):
	def can_handle(self, handler_input):
		logger.info("Lets see... ******")
		return (is_intent_name("GetInformation")(handler_input))
	def handle(self, handler_input):
		speechText = "Lo siento, no me he enterado de nada"	
		logger.info("Evaluating ******")
		intentname = handler_input.request_envelope.request.intent.name
		print('intentname:' + intentname)

		body =  { 'StructureName': 'Parlament 36',
				  'DeviceName': 'Salon',
				  'Action': 'GET'
				}
		logger.info("Calling lambda MELGet ")
		logger.info("With body:" + json.dumps(body))
		response = lambda_client.invoke(FunctionName='MELGet',
										InvocationType='RequestResponse',
										Payload=json.dumps(body))
		res_json = json.loads(response['Payload'].read().decode("utf-8"))	
		print(res_json)
		homeTemp = res_json.get('RoomTemperature')
		homePower = res_json.get('Power')
		if homePower == True:
			homePowerStr = "encendido"
		else:
			homePowerStr = "apagado"
		homeSetTemperature = res_json.get('SetTemperature')
		homeFanSpeed = res_json.get('SetFanSpeed')
		speechText = "<say-as interpret-as=\"interjection\"> Atiende!!!</say-as><break time=\"1s\"/> La temperatura de casa es de <say-as interpret-as=\"unit\">{0}</say-as>  grados, \
		 	          el aire acondicionado está {1} con una temperatura consigna de <say-as interpret-as=\"unit\">{2}</say-as> grados, y \
		 			  el ventilador en la velocidad {3}, \
		 			  Eso es todo lo que te puedo contar,\
					  <break time=\"1s\"/>  \
		 			  <say-as interpret-as=\"interjection\"> ¡Salut!</say-as>.".format(homeTemp,homePowerStr,homeSetTemperature,homeFanSpeed)
		return handler_input.response_builder.speak(speechText).response

class ListItemsIntentGetTemperature(AbstractRequestHandler):
	def can_handle(self, handler_input):
		logger.info("Lets see... ******")
		return (is_intent_name("GetTemperature")(handler_input))
	def handle(self, handler_input):
		speechText = "Lo siento, no me he enterado de nada"	
		logger.info("Evaluating ******")
		intentname = handler_input.request_envelope.request.intent.name
		print('intentname:' + intentname)
		body =  { 'StructureName': 'Parlament 36',
				  'DeviceName': 'Salon',
				  'Action': 'GET'
				}
		logger.info("Calling lambda MELGet ")
		logger.info("With body:" + json.dumps(body))
		response = lambda_client.invoke(FunctionName='MELGet',
										InvocationType='RequestResponse',
										Payload=json.dumps(body))
		res_json = json.loads(response['Payload'].read().decode("utf-8"))	
		print(res_json)
		homeTemp = res_json.get('RoomTemperature')
		homeSetTemperature = res_json.get('SetTemperature')
		speechText = "A ver...!<break time=\"1s\"/>La temperatura de casa es de <say-as interpret-as=\"unit\">{0}</say-as>  grados, \
		 	          con una temperatura objetivo de <say-as interpret-as=\"unit\">{1}</say-as> grados.\
				  	  <break time=\"1s\"/>  \
		 		 	  <say-as interpret-as=\"interjection\">¡Salut!</say-as>.".format(homeTemp,homeSetTemperature)
		return handler_input.response_builder.speak(speechText).response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ListItemsIntent())
sb.add_request_handler(ListItemsIntentFan())
sb.add_request_handler(ListItemsIntentGetInfo())
sb.add_request_handler(ListItemsIntentGetTemperature())


sb.add_exception_handler(AllExceptionsHandler())

handler = sb.lambda_handler()

