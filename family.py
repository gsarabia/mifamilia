from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import datetime
import pytz
import logging
import six
import math

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

timezone = pytz.timezone('America/Mexico_City')

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "<speak>Hola! ¿Que necesitas saber?.</speak>"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Mi Familia", "¿Que necesitas saber?")).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return is_intent_name("AMAZON.HelpIntent")(handler_input)

	def handle(self, handler_input):
		speechText = "Bienvenidos a la ayuda Familia!. Sólo debes preguntarme por un dato familiar"

		return handler_input.response_builder.speak(speechText).response



class CancelOrStopIntentHandler(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return (is_intent_name("AMAZON.CancelIntent")(handler_input) or 
				is_intent_name("AMAZON.StopIntent")(handler_input))
	
	def handle(self, handler_input):
		speechText = "<speak>Hasta la próxima Familia!.</speak>"

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
        print(exception)
        speechText = "<speak><say-as interpret-as=\"interjection\">ehm</say-as>,no he comprendido lo que me has dicho. Di, ayuda, para obtener más información sobre lo que puedo hacer.</speak>"
        return handler_input.response_builder.speak(speechText).response


class BirthdayIntentHandler(AbstractRequestHandler):
    def GetYears(self, current_year, name):
        if name == 'Viole':
            years = current_year - 1978   
        elif name == 'Zuri':
            years = current_year - 2017
        elif name == 'Evan':
            years = current_year - 2015
        else:
            years = current_year - 1984
        
        return years


    def GetData(self, current_year, name):
        if name == 'violeta' or name == 'viole' or name == 'mama':
            next_bd = datetime.datetime(current_year, 8, 25)
            who = 'Viole'
        elif name == 'zuri' or name == 'aylin' or name == 'princesa' or name == 'hermana' or name == 'suri' or name == 'sury':
            next_bd = datetime.datetime(current_year, 10, 31)
            who = 'Zuri'
        elif name == 'evan' or name == 'damir' or name == 'hermano' or name == 'eban':
            next_bd = datetime.datetime(current_year, 7, 28)
            who = 'Evan'
        elif name == 'gil' or name == 'gilberto' or name == 'papa':
            next_bd = datetime.datetime(current_year, 6, 12)
            who = 'Gil'
        else:
            next_bd = None
            who = None
        
        if not next_bd is None:
            next_bd = timezone.localize(next_bd)

        return (who, next_bd)


    def can_handle(self, handler_input):
        return is_intent_name("BirthdayIntent")(handler_input)
	
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        firstname = slots['firstname']

        if firstname is None:
            #no name was given
            speechText = 'De quien quieres saber el cumple'
            return handler_input.response_builder.speak(speechText).response

        today = datetime.datetime.now(timezone)
        current_year = today.year
        
        #keep only date, remove time
        today = datetime.datetime(current_year, today.month, today.day)
        today = timezone.localize(today)

        name = firstname.value.lower()

        (name, next_bd) = self.GetData(current_year, name)
        years = self.GetYears(current_year, name)

        if next_bd is None:
            return handler_input.response_builder.speak("<speak>No se cuando cumpleaños {0}, <lang xml:lang=\"en-US\">sorry</lang></speak>".format(firstname.value)).response

        if today < next_bd:
            days =  next_bd - today
        else:
            days = timezone.localize(datetime.datetime(current_year, next_bd.month, next_bd.day)) - today 
            
        days_left = days.days
        

        if days_left > 0:
            speechText = "<speak>Faltan <say-as interpret-as=\"number\">{0}</say-as> días para el cumple de {1}. El <say-as interpret-as=\"date\" format=\"dm\">{2}-{3}</say-as> cumplira <say-as interpret-as=\"number\">{4}</say-as> años</speak>".format(days_left, name, next_bd.day, next_bd.month, years)
            
            handler_input.response_builder.speak(speechText).set_card(SimpleCard("Mi Familia", "Faltan {0} días para tu cumple {1}, cumpliras {2}".format(days_left, name, years))).set_should_end_session(True)
            return handler_input.response_builder.response
        elif days_left < 0:
            speechText = "<speak>Hace <say-as interpret-as=\"number\">{0}</say-as> días {1} cumplio <say-as interpret-as=\"number\">{2}</say-as> años, exactamente el <say-as interpret-as=\"date\" format=\"dm\">{3}-{4}</say-as></speak>".format(int(math.fabs(days_left)), name, years, next_bd.day, next_bd.month)
            
            handler_input.response_builder.speak(speechText).set_card(SimpleCard("Mi Familia", "{0} ya tienes {1} años.".format(name, years))).set_should_end_session(True)
            return handler_input.response_builder.response
        else:
            speechText = "<speak>Hoy cumples <say-as interpret-as=\"number\">{0}</say-as> años, {1}. Felicidades!!!</speak>".format(years, name)

            handler_input.response_builder.speak(speechText).set_card(SimpleCard("Mi Familia", "Hoy cumples {0} años, {1}. Felicidades!!!".format(years, name))).set_should_end_session(True)
            return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(BirthdayIntentHandler())

sb.add_exception_handler(AllExceptionsHandler())

handler = sb.lambda_handler()