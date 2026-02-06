# what is this?
turns any gif to an animated inventory you can use in minecraft,
requires fabric + [animatica](https://modrinth.com/mod/animatica)

this is right now for only the survival inventory

# how to use
have a gif, rename it to "input.gif" run main.py

after its done you can just copy the "done" folder to your resourcepacks folder

# how to run
## windows
pip install -r requirements.txt

python main.py

## linux/mac
python -m venv venv 

source venv/bin/activate

pip install -r requirements.txt

python main.py

# todo
- [ ] add other inventory types such as creative 
- [ ] add options for lower fire, small shield, small totem, no explosions
- [ ] automatically detect if a gif is an image/1 frame
- [ ] optifine support or finding a way to make it universal


pro tip: if you have a texturepack already made just go to done copy the assets folder and paste in your pre-made texturepack, it will only replace the inventory texture!
