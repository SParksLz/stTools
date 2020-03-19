import sys
import subprocess

from maya import cmds

from ddpmaya import log
from ddpmaya.pb import conf
from media import shoot


class PbCore(object):

    def __init__(self,
                 start_frame=None,
                 end_frame=None,
                 offScreen=True,
                 resolution=None,
                 camera=None,
                 image_output=None,
                 mov_output=None,
                 audio_source=None,
                 audio_offset=None,
                 quality=100,
                 frame=None,
                 frame_padding=4,
                 out_stereo=False):
        """
        :Parameters:
            image_output : str | Path
                location were the images should be generated
            start_frame : int
                playblast start frame
            end_frame : int
                playblast end frame
            offScreen : bool | str
                Enables off screen playblast method in maya
            camera : str
                If not mentioned it takes the active viewport of maya
            resolution : tuple
                Full HD (1980x1080) is the default resolution
                and can be changed as well
            mov_output : str | Path
                Overide movie output file. If this is set, all arrow
                processing is skipped
            audio_source : `str` | `Path` | `list`
                Override audio file. Found via clipTiming/renderConfig. Also
                support arrowURIs
            audio_offset : `int`
                Optional audio offset to use in frames (converted to seconds
                using fps).
                Positive numbers "seek" into the audio the amount. This
                should index into the audio
                at frame "0" for this clipTiming.
            frame: list
                List of frames to blast. One frame specified per flag. When
                specified this flag will override any start/end range.
            out_stereo: `bool`
                generate stereo movie or not.
            rawFrameNumbers: `bool`
                This flag will override the default action and frames will be
                numbered using the actual frames specified ythe -frame or
                -startFrame/-endFrame flags.
        """
        self._image_output = image_output
        self._start_frame = start_frame
        self._end_frame = end_frame
        self._camera = camera
        self._frame_padding = frame_padding
        self._off_screen = offScreen
        self._mov_output = mov_output
        self._audio_source = audio_source
        self._audio_offset = audio_offset
        self._quality = quality
        self._frame = frame
        self._out_stereo = out_stereo

        # for stereo
        self._image_outputL = None
        self._image_outputR = None
        self._mov_outputStereo = None

        if resolution is None:
            self._resolution = conf.RESOLUTION
        else:
            self._resolution = resolution

    @property
    def start_frame(self):
        return self._start_frame

    @property
    def end_frame(self):
        return self._end_frame

    @staticmethod
    def _set_model_panel(camera=''):
        """
        This method will get the current active modelPanel
        and change its camera to the specified one

        :Parameters:
            camera : str
                specific camera name to do a playblast
        """
        if not cmds.about(batch=True):
            mainModelPanel = cmds.getPanel(type='modelPanel')[-1]
            log.info('main model panel:{0}'.format(mainModelPanel))
            cmds.setFocus(mainModelPanel)
            currentPanel = cmds.getPanel(wf=True)
            log.info('current panel:{0}'.format(currentPanel))
            log.info('camera:{0}'.format(camera))
            cmds.modelPanel(currentPanel, edit=True, cam=camera)

    def run(self, play=False, **kwargs):
        """
        Generates playblast image sequence into the specified filepath,
        from the regular behavior of maya this will not pop the fcheck
        viewer to show the playblast you will have to make a movie using
        shoot method to see the plablast
        """
        self._set_model_panel(camera=self._camera)
        log.info('Generating Images')
        out_images = cmds.playblast(format='image',
                                    filename=self._image_output,
                                    sequenceTime=0,
                                    clearCache=True,
                                    viewer=0,
                                    showOrnaments=True,
                                    offScreen=self._off_screen,
                                    forceOverwrite=True,
                                    percent=100,
                                    compression='jpg',
                                    quality=self._quality,
                                    widthHeight=self._resolution,
                                    framePadding=self._frame_padding,
                                    **kwargs)
        log.info('Done generating images: {}'.format(out_images))
        frame_padding = '%04d'
        if sys.platform.startswith('win'):
            # Escape on windows
            frame_padding = '%{}'.format(frame_padding)
        out_images = out_images.replace('####', frame_padding)
        shoot_obj = shoot.Shoot(in_file=out_images,
                    out_file=self._mov_output,
                    ffmpeg_args='-start_number {}'.format(
                        self._start_frame))
        shoot_obj.run()
        shoot_obj.run_mov2mp4(self._mov_output)
        if play:
            cmd = ['rvpush', '-tag', 'playblast', 'merge', self._mov_output]
            cmd = 'rez env rv -c "{}"'.format(' '.join(cmd))
            log.info('Playing movie: {}'.format(cmd))
            try:
                subprocess.check_call(cmd, shell=True)
            except subprocess.CalledProcessError:
                # for the first time to run rvpush.
                log.warning(
                    'It looks like "playblast" tag of rvpush does not exist.')
