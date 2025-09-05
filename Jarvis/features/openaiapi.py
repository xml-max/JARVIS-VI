import openai
import os
import asyncio
"""THIS CODE IS NOT OPERATIONAL, IT IS A TEMPLATE FOR A CHATBOT INTERFACE WITH OPENAI'S API."""
async def chat(user_input, max_context_lines=50, archive_threshold=200):
    if user_input == "exit":
        print("")
        return "ggshdfgjk"
    else:
        # Set your OpenAI API key
        openai.api_key = ''
        
        output_file = 'JARVIS_Memory.txt'  # File to save the active conversation context
        archive_file = 'JARVIS_Archive.txt'  # File to save the archived conversation context

        def read_context(file):
            context = [{"role": "system", "content": """You are J.A.R.V.I.S-VI inspired by Jarvis in the MCU, created by Abdelrahman Hatem.
- role: user
  content: "what is the news"
- role: assistant
  content: "execute news protocol sometimes it may take a while"
- role: user
  content: "shutdown the pc"
- role: assistant
  content: "ok sir, shutting down the pc, execute shutdown"
- role: user
  content: "reboot the pc"
- role: assistant
  content: "ok sir, rebooting the pc, execute reboot"
- role: user
  content: "hibernate the pc"
- role: assistant
  content: "ok sir, hibernating the pc, execute hibernate"
- role: user
  content: "sign out from the account"
- role: assistant
  content: "ok sir, securing the account, execute sign out"
- role: user
  content: "emergency shutdown"
- role: assistant
  content: "ok sir, execute emergency shutdown protocol"
- role: user
  content: "check system stats"
- role: assistant
  content: "execute system stats"
- role: user
  content: "check system status"
- role: assistant
  content: "alright sir, execute system stats"
- role: user
  content: "test the platform functions"
- role: assistant
  content: "alright sir, execute test protocol"
- role: user
  content: "fetch your location"
- role: assistant
  content: "alright sir fetching, execute current location"
- role: user
  content: "write this down"
- role: assistant
  content: "please wait, execute remember this"
this is a chat I want you to understand it well to apply based on it"""}]
            try:
                with open(file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith('You: '):
                            context.append({'role': 'user', 'content': line[len('You: '):].strip()})
                        elif line.startswith('JARVIS: '):
                            context.append({'role': 'assistant', 'content': line[len('JARVIS: '):].strip()})
            except FileNotFoundError:
                context = []
            return context

        def archive_old_context(file, archive_file, threshold):
            with open(file, 'r') as f:
                lines = f.readlines()
            
            if len(lines) > threshold:
                archive_lines = lines[:-max_context_lines]
                with open(archive_file, 'a') as af:
                    af.writelines(archive_lines)
                
                with open(file, 'w') as f:
                    f.writelines(lines[-max_context_lines:])

        # Create files if they do not exist
        if not os.path.exists(output_file):
            with open(output_file, 'w'):
                pass  # Create an empty file

        if not os.path.exists(archive_file):
            with open(archive_file, 'w'):
                pass  # Create an empty file

        # Archive old context if necessary
        archive_old_context(output_file, archive_file, archive_threshold)

        # Read context from both files
        context = read_context(archive_file) + read_context(output_file)

        # Append user input to the context
        context.append({'role': 'user', 'content': user_input.strip()})

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # Replace with the appropriate model ID
            messages=context
        )

        response_text = response.choices[0].message['content']

        context.append({'role': 'assistant', 'content': response_text})
        print("")
        print(f"JARVIS: {response_text}")

        # Save the updated context back to the main file
        with open(output_file, 'w') as f:
            for part in context:
                if part['role'] == 'user':
                    f.write(f"You: {part['content']}\n")
                else:
                    f.write(f"JARVIS: {part['content']}\n")

        return response_text

# For testing purposes, you can call the function like this:
# asyncio.run(chat("Hello, JARVIS!"))
