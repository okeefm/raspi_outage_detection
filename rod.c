#include <avcodec.h>
#include <avformat.h>

int main(int argc, char *argv[]) {
	av_register_all();

	AVFormatContext *pFormatCtx;

	//Open the video file
	if (av_open_input_file(&pFormatCtx, argv[1], NULL, 0, NULL) != 0) {
		return -1; //Couldn't open the file, return failure
	}

	//Retrieve stream information
	if (av_find_stream_info(pFormatCtx) < 0) {
		return -1; //Couldn't find stream information
	}

	//Dump information about file onto standard error
	dump_format(pFormatCtx, 0, argv[1], 0);

	int i;
	AVCodecContext *pCodecCtx;

	//Find the first video stream
	int videoStream=-1;

	for (i=0; i < pFormatCtx->nb_streams; i++) {
		if (pFormatCtx->streams[i]->codec->codec_type==CODEC_TYPE_VIDEO) {
			videoStream = i;
			break;
		}
	}

	if (videoStream == -1) {
		return -1; //Didn't find a video stream
	}

	//Get a pointer to the codec context for the video stream
	pCodecCtx = pFormatCtx->streams[videoStream]->codec;

	AVCodec *pCodec;

	//Find the decoder for the video stream
	pCodec=avcodec_find_decoder(pCodecCtx->codec_id);
	if (pCodec=NULL) {
		fprintf(stderr, "Unsupported Codec!\n");
		return -1; //Codec not found
	}

	//Open codec
	if (avcodec_open(pCodecCtx, pCodec) < 0) {
		return -1; //Could not open codec
	}
}