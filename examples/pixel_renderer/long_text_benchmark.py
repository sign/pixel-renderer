# ruff: noqa: E501
from tqdm import tqdm

from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS
from pixel_renderer import PixelRendererProcessor

# 512 words of lorem ipsum
text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed at ante nec leo condimentum blandit. Vestibulum risus elit, pellentesque at congue in, finibus in lacus. Quisque facilisis eget sapien pretium hendrerit. Donec vestibulum malesuada risus eu pharetra. Donec lectus massa, ultricies in convallis vitae, aliquet ac odio. Praesent id placerat dolor, egestas lobortis lacus. Curabitur quis est egestas, ultricies mauris non, porttitor sapien. Nam tempor et neque non mattis.

Curabitur ac urna erat. Ut dictum nisi a semper auctor. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vestibulum eu massa neque. Aliquam a venenatis erat, ut aliquet enim. Vestibulum elit ipsum, varius ac rutrum et, aliquet non urna. Etiam ligula libero, vehicula tristique nisl sit amet, lobortis tristique dui. In hac habitasse platea dictumst. Praesent malesuada at lorem vitae venenatis. Maecenas eget risus gravida, pretium quam non, vehicula lectus. Sed in risus congue, scelerisque risus ut, suscipit magna. Sed sollicitudin placerat egestas. Quisque fringilla non turpis et congue.

Nunc efficitur massa vel quam dictum, nec vehicula libero aliquam. Integer aliquam magna sed porttitor dictum. Nulla placerat vel ipsum id posuere. Nullam dapibus elit id tellus commodo, non laoreet sem lacinia. Pellentesque a condimentum urna, nec condimentum urna. Integer fermentum viverra commodo. Proin auctor at orci et posuere. Duis iaculis risus purus, sit amet dictum elit finibus vitae. Nunc lobortis, dolor elementum interdum pharetra, libero nulla ultricies lectus, ac iaculis velit mi quis lacus. Praesent quis facilisis mi. Nullam rutrum, lectus ac volutpat gravida, arcu ligula iaculis nisi, eu tincidunt arcu nisl at neque. Suspendisse quis elementum justo. Vivamus eu quam felis. Aenean odio neque, luctus ac quam quis, bibendum ornare risus.

Nullam sit amet venenatis enim. Suspendisse in imperdiet purus, ut dapibus ante. Donec eu viverra ex. Praesent lobortis blandit lorem, sit amet suscipit enim cursus a. Pellentesque non dictum metus, in laoreet mi. Vestibulum vel lectus pretium, interdum justo sit amet, viverra augue. Integer et commodo quam, ut porta enim. Praesent aliquam leo nec sem gravida rutrum. Nunc in dui sit amet ante consectetur ultricies. Sed finibus orci vitae orci fermentum, sit amet consectetur ipsum egestas. Donec lacinia dapibus vulputate. Integer pulvinar euismod erat sit amet lobortis. Suspendisse facilisis porttitor ornare. Aliquam ligula odio, faucibus in vestibulum eget, hendrerit egestas quam. Aenean rhoncus, lectus sed ultrices sodales, est mauris suscipit mi, eu tempor sapien ipsum vel turpis. Curabitur facilisis mi vel egestas dictum.

Ut consectetur, ante at efficitur ultrices, turpis odio dignissim erat, eget bibendum eros diam ac orci. Suspendisse rutrum libero et libero accumsan, vitae auctor urna malesuada. Nam sed vestibulum nisl, vel porttitor neque. Vivamus aliquet porta ante, eu porta velit. Nam vitae luctus tellus. Aliquam erat volutpat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam faucibus arcu diam, sit amet sodales nisl interdum vel. Cras ex sem, laoreet sit amet volutpat sed, placerat sit amet turpis. Nulla et velit quam. Proin consequat metus ac tincidunt facilisis. Nullam vehicula sollicitudin pretium. Vivamus maximus rhoncus turpis, vel vulputate velit placerat id. Nullam ornare fermentum imperdiet. Suspendisse non diam in ex tincidunt blandit.
"""

font_config = FontConfig(sources=FONTS_NOTO_SANS)
pixel_processor = PixelRendererProcessor(font=font_config)

# Rendered shape: (16, 19072, 3)
print(pixel_processor.render_text(text).shape)

# Single threaded, ~850it/s
for _ in tqdm(range(10000)):
    pixel_processor.render_text(text)
