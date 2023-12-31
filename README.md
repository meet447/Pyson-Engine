﻿# Pyson-Engine

Welcome to the Pyson Novel Engine using Pygame! This sophisticated engine empowers you to craft captivating interactive stories by seamlessly blending dynamic characters, engaging dialogues, and consequential choices. Dive into the realm of storytelling as you create your own captivating scenes and narratives using JSON data and the formidable capabilities of the Pygame library.

## Getting Started

### Prerequisites

1. **Python Installation**: Ensure you have Python 3.x installed on your system. If not, you can download it from [Python's official website](https://www.python.org/downloads/).

2. **Pygame Installation**: Install the Pygame library by executing the following command in your terminal:

```bash
pip install pygame
```

### Scene Creation using JSON Data

1. Open the `scenes.json` file and initiate the process of crafting your visual novel's narrative canvas.

2. Begin by creating scenes, setting the ambiance with backgrounds, and infusing life into your characters with their dialogues and interactions.

```json
"scenes": [
   {
       "background": "sprites/background.jpg",
       "dialogues": [
           {
               "speaker": "Saber",
               "text": "Hello, welcome to our adventure!"
           },
           {
               "speaker": "Jack",
               "text": "Indeed, it's going to be exciting."
           }
       ],
       "characters": [
           {
               "sprite": "sprites/jack.png",
               "x": 100,
               "width": 400,
               "height": 600
           },
           {
               "sprite": "sprites/jack.png",
               "x": 1200,
               "side": "right",
               "width": 400,
               "height": 600
           }
       ],
       "choices": [
           {
               "text": "Let's go on an adventure!",
               "next_scene": 1
           },
           {
               "text": "I'm not sure...",
               "next_scene": 2
           }
       ]
   },
   // More scenes...
]
```

3. Customize your visual novel's text boxes using the `text_box_style` option. Adjust background color, border color, width, and transparency to craft an immersive reading experience.

## Running the Engine

1. Modify the `scenes.json` file to meticulously craft your novel's storyline.

2. Run the engine by executing the `main.py` script using Python. Watch as your visual novel springs to life, offering you an avenue to engage and interact.

## How to Engage with Your Novel

- Utilize the Space key to navigate through dialogues, unravelling the narrative at your own pace.
- Employ number keys to select choices, shaping the course of the story with your decisions.
- Employ mouse clicks to interact with characters and their surroundings, enhancing the immersive experience.

## Creating Your Own Visual Novel

1. **Crafting Scenes and Dialogues**: Create a symphony of captivating scenes, setting the stage with backgrounds, vivid dialogues, and interactive characters.

2. **Consequential Choices**: Add depth to your narrative by incorporating meaningful choices. Define the text and corresponding scenes to which each choice leads.

3. **Text Box Customization**: Enrich the visual experience by customizing text box styles using the `text_box_style` option. Tailor background color, border style, width, and transparency.

4. **Testing and Tweaking**: Run the engine to test your novel's flow. Observe how dialogues and choices come together to create a seamless, interactive storyline.

## Detailed Example Scenario

1. **The Adventure Unfolds**: Construct the opening scene by introducing dynamic dialogues for characters, setting the tone for the forthcoming journey.

2. **Meaningful Choices**: Present players with choices, allowing them to define the course of the narrative. Craft choices that resonate with the unfolding story.

3. **Journey into Mystery**: Create a captivating new scene with a distinctive background and character. Lead characters into an enigmatic forest, heightening curiosity.

4. **Choice Shaping the Tale**: Shape the storyline with choices that propel characters into different directions. Develop choices that imbue the story with excitement.

5. **Discovering the Hidden**: Craft an atmosphere of discovery with dialogues and character interactions. Unveil hidden entrances and the allure of the unknown.

6. **Choices with Impact**: Design choices that influence characters' decisions, leading them either into the heart of mystery or compelling them to wait and watch.

7. **Reaping the Rewards**: Craft a scene that reveals the fruit of characters' endeavors. Express achievement and fulfillment through well-crafted dialogues.

8. **Final Reflections**: Conclude the story by framing characters' perspectives and reflecting on the adventure's significance. Captivate players until the very end.

## Conclusion

The Visual Novel Engine using Pygame elevates storytelling to new heights. Seamlessly blend dialogues, characters, and choices using JSON data, then bring your narrative to life with the Pygame library. Whether you're a storyteller or an audience, dive into this captivating world of interactive stories, and be prepared to embark on a journey of emotions, decisions, and limitless creativity.
