# MachineBBQ

I. Input requirement spec.<br>
  Aim:<br>
    This project aims to automate the translation of videos on YouTube for 推しのVTubers.<br>

II. Output requirement spec.<br>
  Procedure:<br>
    1. download video/audio from YouTube to the local environment.<br>
    2. convert video/audio  to text format.<br>
    3. get time serial audio information and align it to the text file.<br>
    4. translate acquired text files.<br>
    5. check the correctness of translated scrips.<br>
    6. add translated subtitles to the video.<br>
    7. verification.<br>

III. Validation<be>
(Empty)

Known issues:
1. The subtitles auto-generated by YouTube may not be suitable for following processing sometimes, such as misspelling or Sentence segmentation error.
2. Video download and voice recognition are currently functional for "DL_VoiceRec.py".

