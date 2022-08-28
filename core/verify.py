import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'],os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])
kr_phone_prefix = "+82"
def send(phone):
    verify.verifications.create(to=kr_phone_prefix+phone[1:], channel='sms')

def check(phone, code):
    try:
        result = verify.verification_checks.create(to=kr_phone_prefix+phone[1:], code=code)
        print(result)
    except TwilioRestException as e:
        # print("Failed Verfication", e.status)

        return False, e.status
    return result.status == 'approved', 200