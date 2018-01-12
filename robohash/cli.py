import argparse
import io
import sys
from robohash import Robohash


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--set", default="set1")
  parser.add_argument("-x", "--width", type=int, default=300)
  parser.add_argument("-y", "--height", type=int, default=300)
  parser.add_argument("-f", "--format", default="png")
  parser.add_argument("-b", "--bgset")
  parser.add_argument("-o", "--output", default="robohash.png")
  parser.add_argument("text", help="Text to use for the hash")
  
  args = parser.parse_args()
  
  robohash = Robohash(args.text)
  robohash.assemble(roboset=args.set, bgset=args.bgset,
  					sizex=args.width, sizey=args.height)
  
  robohash.img.save(args.output, format=args.format)

if __name__ == "__main__":
    main()
