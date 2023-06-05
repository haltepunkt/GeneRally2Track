from dataclasses import dataclass
from struct import *
import argparse, json, os

@dataclass
class Track:
  name: str
  author: str
  comments: str
  water_level: int
  view_angle: int
  rotation: int
  zoom: int
  world_size: int

argument_parser = argparse.ArgumentParser(description='Print details of GeneRally 2 tracks')

argument_parser.add_argument('track')
argument_parser.add_argument('--json', action='store_true', default=False)

arguments = argument_parser.parse_args()

with open(arguments.track, 'rb') as track_file:
  buffer = track_file.read()

  signature_format = '6s'
  signature_size = calcsize(signature_format)

  signature = unpack(signature_format, buffer[0:signature_size])[0].decode('utf-8')

  if signature == 'GR2TRK':
    properties_offset = 0x5F
    properties_format = 'BBHBB'
    properties_size = calcsize(properties_format)

    water_level, view_angle, rotation, zoom, world_size = unpack(properties_format, buffer[properties_offset:properties_offset + properties_size])

    strings_offset = 0x65

    name_offset = strings_offset
    name_length_format = 'B'
    name_length = unpack(name_length_format, buffer[name_offset:name_offset + 1])[0]
    name_format = f'{name_length}s'

    name = unpack(name_format, buffer[name_offset + 1:name_offset + 1 + name_length])[0].decode('utf-8')

    author_offset = name_offset + 1 + name_length
    author_length_format = 'B'
    author_length = unpack(author_length_format, buffer[author_offset:author_offset + 1])[0]
    author_format = f'{author_length}s'

    author = unpack(author_format, buffer[author_offset + 1:author_offset + 1 + author_length])[0].decode('utf-8')

    comments_offset = author_offset + 1 + author_length
    comments_length_format = 'B'
    comments_length = unpack(comments_length_format, buffer[comments_offset:comments_offset + 1])[0]
    comments_format = f'{comments_length}s'

    comments = unpack(comments_format, buffer[comments_offset + 1:comments_offset + 1 + comments_length])[0].decode('utf-8')

    track = Track(
      name, author, comments,
      water_level, view_angle, rotation, zoom, world_size
    )

    if arguments.json:
      print(json.dumps(track.__dict__))
    else:
      print(f'File name:\t{os.path.basename(arguments.track)}')
      print(f'File signature:\t{signature}')
      print('')
      print(f'Name:\t\t{track.name}')
      print(f'Author:\t\t{track.author}')
      print(f'Comments:\t{track.comments}')
      print('')
      print(f'Water level:\t{track.water_level}')
      print(f'View angle:\t{track.view_angle}')
      print(f'Rotation:\t{track.rotation}')
      print(f'Zoom:\t\t{track.zoom}')
      print(f'World size:\t{track.world_size}')
