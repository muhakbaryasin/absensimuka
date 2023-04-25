from av import VideoFrame
from aiortc import MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay
from aiortc.rtcrtpsender import RTCRtpSender
import platform


class VideoTransformTrack(MediaStreamTrack):
    relay = None
    webcam = None
    """
    A video stream track that transforms frames from another track.
    """

    kind = "video"

    def __init__(self, track):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")

        # rebuild a VideoFrame, preserving timing information
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame

    @staticmethod
    def create_local_tracks(play_from, decode):
        relay = VideoTransformTrack.relay
        webcam = VideoTransformTrack.webcam

        if play_from:
            player = MediaPlayer(play_from, decode=decode)
            return player.audio, player.video
        else:
            options = {"framerate": "30", "video_size": "640x480"}
            if relay is None:
                if platform.system() == "Darwin":
                    webcam = MediaPlayer(
                        "default:none", format="avfoundation", options=options
                    )
                elif platform.system() == "Windows":
                    webcam = MediaPlayer(
                        "video=Integrated Camera", format="dshow", options=options
                    )
                else:
                    webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
                relay = MediaRelay()
            return None, relay.subscribe(webcam.video)

    @staticmethod
    def force_codec(pc, sender, forced_codec):
        kind = forced_codec.split("/")[0]
        codecs = RTCRtpSender.getCapabilities(kind).codecs
        transceiver = next(t for t in pc.getTransceivers() if t.sender == sender)
        transceiver.setCodecPreferences(
            [codec for codec in codecs if codec.mimeType == forced_codec]
        )
