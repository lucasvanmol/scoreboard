"""Create PNG images for various types of scoreboards.

Usage
-----

    from scoreboard import Leaderboard

    ranking = [
        ("Player 1", 30),
        ("Player 2", 15),
        ("Player 3", 50)
    ]

    # Save png image
    lb = Leaderboard(ranking)
    lb.save_image("leaderboard.png")

    # Save base 64 encoded image
    b64_leaderboard = lb.b64_image()
    with open("images/image.b64", "wb") as f:
        f.write(b64_leaderboard)
"""
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from abc import ABC, abstractmethod
import base64

# Type alias for RGBA colors
Color = tuple[float, float, float, float]

class Scoreboard(ABC):
    """Base class for scoreboard creation. Use a child class to define its behaviour."""

    @property
    def image(self) -> Image:
        return self._generate_image()

    def b64_image(self) -> bytes:
        """Generate the image and encode in base64
        

        Returns
        -------
            Base64 encoded image data in bytes
        """
        buffer = BytesIO()
        self.image.save(buffer, "PNG")   
        im_b64 = base64.b64encode(buffer.getvalue())
        im_b64 = b"data:image/png;base64," + im_b64
        return im_b64

    def save_image(self, file_name: str):
        """Save the image to a file
        
        Params
        ------
            file_name:
                Name of the file. The file is saved as .png and other extensions will be ignored.
        """
        if not file_name.endswith(".png"):
            file_name += ".png"
        self.image.save(file_name)
    
    @classmethod
    def fit_text_to_length(cls, text: str, font: ImageFont, max_length: int) -> ImageFont:
        font_size = font.size
        
        
        while font.getlength(text) > max_length and font_size > 1:
            font_size -= 1
            font = font.font_variant(size=font_size)
        
        return font

    @abstractmethod
    def _generate_image(self) -> Image:
        pass


class Leaderboard(Scoreboard):
    """Create a ranking of players with optional title

    Leaderboard will automatically sort players based on their scores.

    Attributes
    ----------
    ranking : [(str, float), ... ]
        a list of (str, float) tuples where:
            str is the player's displayed name
            float is the player's score
    """

    def __init__(
            self,
            ranking: list[tuple[str, float]],
            fill_color: Color = (255, 249, 251, 0),
            text_color: Color = (65, 101, 138, 255),
            text_color_alternate: Color = (102, 143, 183, 255),
            seperator: bool = True,
            seperator_color: Color = (106, 107, 120),
            seperator_width: int = 5,
            font_file: str = "open-sans/OpenSans-Regular.ttf",
            font_file_bold: str = "open-sans/OpenSans-Bold.ttf",
            font_size: int = 72,
            margin_left: int = 50,
            margin_right: int = 50,
            margin_top: int = 50,
            margin_bot: int = 50,
            line_spacing: int = 25,
            title: str = None,
            title_font_size: int = 112
        ):

        super().__init__()
        self.ranking = ranking
        self.fill_color = fill_color
        self.text_color = text_color
        self.text_color_alternate = text_color_alternate
        self.seperator = seperator
        self.seperator_color = seperator_color
        self.seperator_width = seperator_width
        self.font_file = font_file
        self.font_file_bold = font_file_bold
        self.font_size = font_size
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.margin_bot = margin_bot
        self.line_spacing = line_spacing
        self.title = title
        self.title_font_size = title_font_size

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value: list[tuple[str, float]]):
        value.sort(key=lambda player: player[1], reverse=True)
        self._ranking = value

    def _generate_image(self) -> Image:
        font = ImageFont.truetype(self.font_file, self.font_size)
        font_bold = ImageFont.truetype(self.font_file_bold, self.font_size)

        # Add font_size to margin top due to anchor of text being at baseline
        # also increase margin for when there's a title
        if self.title:
            title_font = font_bold.font_variant(size=self.title_font_size)
            adjusted_margin_top = self.margin_top + self.title_font_size
            titleMarginTop = adjusted_margin_top
            adjusted_margin_top += title_font.getsize(self.title)[1]
        else:
            adjusted_margin_top = self.margin_top + self.font_size

        width = 800
        img_size = (width, adjusted_margin_top + self.margin_bot + (len(self.ranking)-1) * (self.font_size + self.line_spacing) + self.line_spacing)
        image = Image.new("RGBA", img_size, self.fill_color)
        draw = ImageDraw.Draw(image)
        

        if self.title:
            draw.text(
                (img_size[0]/2, titleMarginTop),
                self.title,
                font=title_font,
                fill=self.text_color,
                anchor="ms"
            )

        for i, entry in enumerate(self.ranking):
            color = [self.text_color, self.text_color_alternate][i%2]

            # Number
            numberText = f"{i+1}  "
            draw.text(
                (self.margin_left, adjusted_margin_top + i*(self.font_size + self.line_spacing)),
                numberText,
                font=font,
                fill=color,
                anchor="ls"
            )

            # Score
            scoreText = " " +str(entry[1])
            draw.text(
                (img_size[0] - self.margin_right, adjusted_margin_top + i*(self.font_size+self.line_spacing)),
                scoreText,
                font=font,
                fill=color,
                anchor="rs"
            )

            # Name
            nameText = entry[0]
            numberTextLength = font.getlength(numberText)
            scoreTextLength = font.getlength(scoreText)
            maxLength = img_size[0] - self.margin_left - self.margin_right - numberTextLength - scoreTextLength
            
            nameFont = Leaderboard.fit_text_to_length(nameText, font_bold, maxLength)

            draw.text(
                (self.margin_left + numberTextLength, adjusted_margin_top + i*(self.font_size+self.line_spacing)),
                nameText,
                font=nameFont,
                fill=color,
                anchor="ls"
            )

            # Seperator
            if self.seperator:
                draw.line(
                    [
                        (self.margin_left, adjusted_margin_top + (i-0.75)*(self.font_size+self.line_spacing)),
                        (img_size[0] - self.margin_right, adjusted_margin_top + (i-0.75)*(self.font_size+self.line_spacing))
                    ],
                    fill=self.seperator_color,
                    width=self.seperator_width
                )

        # Extra seperator at end
        if self.seperator:
                draw.line(
                    [
                        (self.margin_left, adjusted_margin_top + (i+0.25)*(self.font_size+self.line_spacing)),
                        (img_size[0] - self.margin_right, adjusted_margin_top + (i+0.25)*(self.font_size+self.line_spacing))
                    ],
                    fill=self.seperator_color,
                    width=self.seperator_width
                )

        return image

class Head2Head(Scoreboard):
    """Create a scoreboard comparing teams/players without ranking.

    Useful for team vs team situations, or keeping track of a combined score
    when used with only one team.

    Attributes
    ----------
    teams : [(str, float), ... ]
        a list of (str, float) tuples where:
            str is the player or team's displayed name
            float is the player or teams's score
    """

    def __init__(
            self,
            teams: list[tuple[str, float]],
            fill_color: Color = (255, 249, 251, 0),
            text_color: Color = (65, 101, 138, 255),
            score_color: Color = (102, 143, 183, 255),
            font_file: str = "open-sans/OpenSans-Regular.ttf",
            font_file_bold: str = "open-sans/OpenSans-Bold.ttf",
            font_size: int = 72,
            score_font_size: int = 160,
            title: str = None,
            title_font_size: int = 112,
            margin_sides: int = 50,
            rectangle: bool = True,
            rectangle_margin: int = 50,
            rectangle_color: Color = (102, 143, 183, 255)
        ):

        super().__init__()
        self.teams = teams
        self.fill_color = fill_color
        self.text_color = text_color
        self.score_color = score_color
        self.font_file = font_file
        self.font_file_bold = font_file_bold
        self.font_size = font_size
        self.score_font_size = score_font_size
        self.title = title
        self.title_font_size = title_font_size
        self.margin_sides = margin_sides
        self.rectangle = rectangle
        self.rectangle_margin = rectangle_margin
        self.rectangle_color = rectangle_color

    def _generate_image(self) -> Image:

        score_font = ImageFont.truetype(self.font_file, self.score_font_size)
        team_font = ImageFont.truetype(self.font_file_bold, self.font_size)
        if self.title:
            title_font = ImageFont.truetype(self.font_file_bold, self.title_font_size)

        component_size = [0, 500]
        for team in self.teams:
            name_length = int(team_font.getlength(team[0])) + self.margin_sides
            if name_length > component_size[0]:
                component_size[0] = name_length


        img_size = (component_size[0] * len(self.teams), component_size[1])
        image = Image.new("RGBA", img_size, self.fill_color)
        draw = ImageDraw.Draw(image)

        if self.title:
            draw.text(
                (img_size[0]/2, img_size[1]/5),
                self.title,
                font=title_font,
                anchor='ms',
                fill=self.text_color
            )

        x_spacing = float(img_size[0]) / len(self.teams)
        for i, team in enumerate(self.teams):
            x_coord = x_spacing/2 + i*x_spacing
            draw.text(
                (x_coord, component_size[1] / (3 if self.title else 4)),
                team[0],
                font=team_font,
                anchor='mm',
                fill=self.text_color
            )

            score_margin = self.margin_sides + self.rectangle_margin if self.rectangle else self.margin_sides
            adjusted_score_font = Scoreboard.fit_text_to_length(str(team[1]), score_font, component_size[1] - score_margin)

            score_coords = (x_coord, component_size[1] * 2 / 3) # Center of score str & bounding rectangle
            draw.text(
                score_coords,
                str(team[1]),
                font=adjusted_score_font,
                anchor='mm',
                fill=self.score_color
            )
            bbox = adjusted_score_font.getbbox(str(team[1]),anchor='mm')

            if self.rectangle:
                draw.rounded_rectangle(
                    (bbox[0]+score_coords[0] - self.rectangle_margin, bbox[1]+score_coords[1] - self.rectangle_margin,
                    bbox[2]+score_coords[0] + self.rectangle_margin, bbox[3]+score_coords[1] + self.rectangle_margin),
                    outline=self.rectangle_color,
                    radius=10,
                    width=10,
                )
        
        return image
