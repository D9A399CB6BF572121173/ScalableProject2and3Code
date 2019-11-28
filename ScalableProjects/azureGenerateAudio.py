#!/usr/bin/env python3
import os
import requests
from xml.etree import ElementTree 
import os
import random
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', help='Length of captchas in characters', type=int)
    parser.add_argument('--count', help='How many captchas to generate', type=int)
    parser.add_argument('--output-dir', help='Where to store the generated captchas', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()
    
    if args.length is None:
        print("Please specify the captcha length")
        exit(1)

    if args.count is None:
        print("Please specify the captcha count to generate")
        exit(1)

    if args.output_dir is None:
        print("Please specify the captcha output directory")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Generating captchas with symbol set {" + captcha_symbols + "}")

    if not os.path.exists(args.output_dir):
        print("Creating output directory " + args.output_dir)
        os.makedirs(args.output_dir)

# Creating audio files for training purpose with the help of google text to speech
    for i in range(args.count):
            #taking random strings
        captcha_text = ''.join([random.choice(captcha_symbols) for j in range(args.length)])
        #generating mp3 audio files
        audio_path = os.path.join(args.output_dir, captcha_text)
        
        # subscription details
        subscription_key = "0c49f817f91340ad88982c446dca9533"
        tts = captcha_text
        access_token = None
        
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
          }
        response = requests.post(fetch_token_url, headers=headers)
        access_token = str(response.text)
        
        
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'ArzooResourceAzure'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
        'name', 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)')
        voice.text = tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
                    with open(audio_path + '.wav', 'wb') as audio:
                            audio.write(response.content)
                            print("\nStatus code: " + str(response.status_code) +
                  "\nYour TTS is ready for playback.\n")
        else:
                                print("\nStatus code: " + str(response.status_code) +
                                      "\nSomething went wrong. Check your subscription key and headers.\n")
        

        print(audio_path)
        

if __name__ == '__main__':
    main()
