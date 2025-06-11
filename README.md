# RoboHash

The source code for [RoboHash.org](https://robohash.org/).

This tool generates unique images from a given string of text.

Put in any text, such as IP address, email, filename, userid, or whatever else you like, and get back a robot/alien/monster/cat/human image for your site. With hundreds of millions of variations, Robohash is among the leading robot-based hashing tools on the web.

It operates by algorithmically assembling various robot components together, using bits from the SHA hash. Not perfect, not entirely secure, but it gives a good gut-check to "Hey, this SHA is wrong."

# Ways to Use Robohash

There are several ways to use Robohash, depending on your needs:

## 1. Using the Public Service

The easiest way to use Robohash is through the public service at [robohash.org](https://robohash.org/).

Super Easy to use: Anytime you need a Robohash, just embed:

```html
<img src="https://robohash.org/YOUR-TEXT.png" />
```

**URL Parameters and Advanced Options:**

- **Image Formats**: Want a JPG instead? Fine. PNG? Fine. Want it as a bitmap? We think you're nutty. But fine.
  Just change the extension: `https://robohash.org/hash.jpg`
- **Size Control**: From destroying skyscrapers to nanobots, we've got you covered.
  `https://robohash.org/hash?size=200x200`
- **Robot Sets**: Choose your preferred mechanical beings:
  `https://robohash.org/hash?set=set2` (set1-set5 available, or "any")
- **Backgrounds**: Our robots like to travel. Add a background as part of the hash:
  `https://robohash.org/hash?bgset=bg1` (bg1-bg2 available, or "any")
- **Gravatar Integration**: For Gravatar enthusiasts, you can ask Robohash to use a Gravatar if one is available:
  `https://robohash.org/user@example.com?gravatar=yes`
  or for pre-hashed emails: `https://robohash.org/hash?gravatar=hashed`
- **Directory Style Parameters**: We also accept commands via directory structure:
  `https://robohash.org/set_set3/bgset_bg1/3.14159?size=500x500`
- **Extension Handling**: Want to hash the whole URL including extension? Use:
  `https://robohash.org/hash.png?ignoreext=false`

**Important Notes:**

- Robohash.org is a best-effort service, not a commercial offering
- Our robots stay speedy due to caching modules and CDN usage
- If you receive errors or "too many requests" responses, please back off exponentially
- For high-volume or production use, consider hosting your own instance using Docker
- Very infrequent murderous rampages (that's a fact!)

## 2. Using Pre-built Docker Images

For the simplest self-hosted solution, use our pre-built Docker images:

```bash
# Pull the latest version
docker pull ghcr.io/e1ven/robohash:latest

# Run the container
docker run -p 8080:8080 ghcr.io/e1ven/robohash:latest
```

Your Robohash instance will be available at `http://localhost:8080`

## 3. Building Your Own Docker Image

If you want to customize the Docker image:

```bash
# Clone the repository
git clone https://github.com/e1ven/Robohash.git
cd Robohash

# Build the image
docker build -t robohash .

# Run the container
docker run -p 8080:8080 robohash
```

## 4. Python Library (Programmatic Usage)

For integration in Python applications, install the library:

```bash
pip install robohash
```

Then use it in your code:

```python
from robohash import Robohash

# Create a robot for any text
hash_text = "example@example.com"
rh = Robohash(hash_text)

# Customize your robot (all parameters optional)
rh.assemble(
    roboset='set1',        # Which set to use (set1-set5 or 'any')
    color=None,            # Color for set1 (only works with set1)
    format='png',          # Output format (png, jpg, etc)
    bgset=None,            # Background set (bg1, bg2, or None)
    sizex=300,             # Width
    sizey=300              # Height
)

# Save to file
with open("robot.png", "wb") as f:
    rh.img.save(f, format="png")
```

## 5. Web Frontend (Self-Hosted Service)

To run the web service on your own server:

```bash
# Install the package with web dependencies
pip install robohash[web]

# Run the web service (defaults to port 80)
python -m robohash.webfront
```

You can specify a different port:

```bash
PORT=8080 python -m robohash.webfront
```

## Development

Dependencies are managed using requirements.in and pip-compile:

```bash
$ pip install pip-tools
$ pip-compile requirements.in  # Updates requirements.txt with pinned versions
$ pip install -r requirements.txt
```

## Usage

```python
from robohash import Robohash

hash = "whatever-hash-you-want"
rh = Robohash(hash)
rh.assemble(roboset='any')
with open("path/to/new/file.png", "wb") as f:
    rh.img.save(f, format="png")
```

## Robosets

RoboHash comes with five distinct sets of mechanical/biological entities:

- **set1**: Classic robots created by Zikri Kader. The original robotic workforce.
- **set2**: Monsters created by Hrvoje Novakovic. A whole slew of random monsters.
- **set3**: Robot heads created by Julian Peter Arias. New, suave, disembodied heads. That's sexy. Like a robot.
- **set4**: Cats created by David Revoy. Hydroponically grown beautiful kittens.
- **set5**: Human avatars created by Pablo Stanley. For those afraid of the robocalypse, you can also generate human technicians to mind the robot army.
- **set6**: Cosmic Apes created by OceanSlim. Monkeying around with the fabric of space-time itself.
  - Note: This set uses additional symbolic links to implement weighted rarity distribution as the creator originally intended. Apes with laser eyes and tear drop tattoos are exceptionally rare.

Specify which set you want in the `assemble()` method or through URL parameters. Alternatively, specify the string "any", and RoboHash will pick an image set for you, based on the provided hash.

If you use a specific set, or a list of them (like "?sets=1,3"), it'll probably stay the same as it is now. If you use "set=any", it'll include any new sets we happen to add, so existing hashes may change.

## License

The Python Code is available under the MIT/Expat license. See the `LICENSE.txt` file for the full text of this license. Copyright (c) 2011.

Feel free to embed the Robohash images, host your own instance of Robohash, or integrate them into your own project. If you do, please just mention where they came from :) Example wording might be "Robots lovingly delivered by Robohash.org" or similar.

### Image Sets Attribution

Robohash contains art from various talented creators:

- The "set1" artwork (and robohash backgrounds) were created by Zikri Kader. They are available under CC-BY-3.0 or CC-BY-4.0 license.
- The "set2" artwork was created by Hrvoje Novakovic. They are available under CC-BY-3.0 license.
- The "set3" artwork was created by Julian Peter Arias. They are available under CC-BY-3.0 license.
- The Cats/"set4" were created by David Revoy, used under CC-BY-4.0 https://www.peppercarrot.com/extras/html/2016_cat-generator/
- The avatars used in "set5" were created by Pablo Stanley, for https://avataaars.com/. They are "Free for personal and commercial use. 😇"
- The Cosmic Apes/"set6" were created by [OceanSlim](https://github.com/0ceanSlim). They are available under CC0 (Public Domain).

You are free to embed robots under the terms of the CC-BY license. Example wording might be "Robots lovingly delivered by Robohash.org" or something similarly respectful of our robotic overlords.

## Continuous Integration and Deployment

This project uses GitHub Actions for continuous integration and deployment:

1. When a tag is pushed (e.g., `v2.0.0`), a Docker image is automatically built and published to GitHub Container Registry
2. Images are tagged with both the specific version and `latest`
3. All container builds are publicly available

The automated workflow makes it easy to deploy new versions without manual building.

## Project Status

This project is considered mostly feature-complete and in maintenance mode. It's fun, and it does what it was designed to do - While I'm happy to fix critical bugs, I'm not actively developing new features or major enhancements.

The original project this was created for is no longer active, and Robohash continues to exist as a standalone service and library that accomplishes its core mission effectively.

Pull requests are welcome, but please understand that I may not be able to review or incorporate them in a timely manner, if at all. This isn't because I don't value your contributions, but simply reflects the reality of the project's lifecycle and my available time.

If you find Robohash useful, I encourage you to fork it and adapt it to your needs. The MIT license makes this easy, and I'm genuinely happy to see the project live on in other forms. Please remember that while the code is MIT licensed, the artwork in the various sets is under different Creative Commons licenses as detailed in the License section above. If you fork this project, be sure to respect these licenses and provide appropriate attribution.

## Original Disclaimer

OK, I'll admit I'm a crappy programmer. Compounding this, I wrote this code initially to be internal-only. It's ugly, and could be a LOT nicer.

Sorry about that.
