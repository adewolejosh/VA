### Voice Assistant

was essentially supposed to be a THA, but seemed like a WRF, hence just going to 
push to Github. A simple Flask API, which has endpoints to transcribe speech-to-text, 
and an endpoint to reply your transcribed speech. Uses open-sourced OpenAI whisper
to transcribe your uploaded speech to text and uses google's Gemini SDK (must get 
a token from Google) to get a AI response on your speech.


##### --- If going to extend 

maybe add authentication, authorization ...  
which leads to adding context and context switching ...  
and which means, users should be able to follow through their previous convo.

and in the AI field maybe adding more training data using the convo to understand, more, your users use-cases.   

something interesting might be creating a webpage help-desk, with something such as this API, where you feed in content of the page to the AI and when users have a question from that page using speech-to-text we can help them
and interesting text-to-speech to answer back. 


##### Setup
Ensure to use Python3.9 thereabout, or you run into issues using whisper.  
Also you need to follow whisper's doc, whilst noting you need to install ffmpeg.  
install, flask, and google gemini api sdk  
then you can simply run locally 

`
flask run --debug
`

