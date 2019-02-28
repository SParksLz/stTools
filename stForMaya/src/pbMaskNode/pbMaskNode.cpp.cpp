#include "pbMaskNode.h"


//pbDrawManager
pbDrawManager::pbDrawManager()
{
}
pbDrawManager::~pbDrawManager()
{
}


MTypeId		pbDrawManager::id(0x0008077A);
MObject		pbDrawManager::attr_transparency;
MObject		pbDrawManager::attr_camera;
MObject		pbDrawManager::attr_Frame;
MObject		pbDrawManager::attr_sizeOfH;
MObject		pbDrawManager::attr_sizeOfW;
MObject		pbDrawManager::attr_Scratchablelatex;
MObject		pbDrawManager::attr_Scratchablelatex_color;
MObject		pbDrawManager::attr_topBorder_cb;
MObject		pbDrawManager::attr_topBorder_col;
MObject		pbDrawManager::attr_bottomBorder_cb;
MObject		pbDrawManager::attr_bottomBorder_col;
MObject		pbDrawManager::attr_border_height;

//toptext
MObject		pbDrawManager::attr_topText_01;
MObject		pbDrawManager::attr_topText_02;
MObject		pbDrawManager::attr_topText_03;
MObject		pbDrawManager::attr_topText_01_cb;
MObject		pbDrawManager::attr_topText_02_cb;
MObject		pbDrawManager::attr_topText_03_cb;
MObject		pbDrawManager::attr_topText_01_w;
MObject		pbDrawManager::attr_topText_02_w;
MObject		pbDrawManager::attr_topText_03_w;
MObject		pbDrawManager::attr_topText_01_color;
MObject		pbDrawManager::attr_topText_02_color;
MObject		pbDrawManager::attr_topText_03_color;
MObject		pbDrawManager::attr_topText_01_showFrame;
MObject		pbDrawManager::attr_topText_02_showFrame;
MObject		pbDrawManager::attr_topText_03_showFrame;
//bottomtext
MObject		pbDrawManager::attr_bottomText_01;
MObject		pbDrawManager::attr_bottomText_01_cb;
MObject		pbDrawManager::attr_bottomText_01_w;
MObject		pbDrawManager::attr_bottomText_01_color;
MObject		pbDrawManager::attr_bottomText_02;
MObject		pbDrawManager::attr_bottomText_02_cb;
MObject		pbDrawManager::attr_bottomText_02_w;
MObject		pbDrawManager::attr_bottomText_02_color;
MObject		pbDrawManager::attr_bottomText_03;
MObject		pbDrawManager::attr_bottomText_03_cb;
MObject		pbDrawManager::attr_bottomText_03_w;
MObject		pbDrawManager::attr_bottomText_03_color;
MObject		pbDrawManager::attr_bottomText_01_showFrame;
MObject		pbDrawManager::attr_bottomText_02_showFrame;
MObject		pbDrawManager::attr_bottomText_03_showFrame;



MString		pbDrawManager::drawDbClassification("drawdb/geometry/pbDrawManager");
MString		pbDrawManager::drawRegistrantId("pbDrawManagerPlugin");
MStatus pbDrawManager::initialize()
{
	MStatus							status;
	MFnNumericAttribute		nAttr;
	MFnTypedAttribute			typedAttr;
	MFnStringData				stringFn;


	//Scratchablelate
	attr_Scratchablelatex = nAttr.create("Scratchable_latex", "sl", MFnNumericData::kBoolean, 1);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_Scratchablelatex);

	//Scratchablelate color
	attr_Scratchablelatex_color = nAttr.create("Scratchable_latex_color", "sl_cd", MFnNumericData::k3Float);
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(0.5f, 0.5f, 0.5f);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_Scratchablelatex_color);

	//top border enable
	attr_topBorder_cb = nAttr.create("Top_border_enable", "tbe", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_topBorder_cb);

	//top border color
	attr_topBorder_col = nAttr.create("Top_border_color", "tbc", MFnNumericData::k3Float);
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(0.5f, 0.5f, 0.5f);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_topBorder_col);


	//bottom border enable
	attr_bottomBorder_cb = nAttr.create("Bottom_border_enable", "bbe", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_bottomBorder_cb);

	//bottom border color
	attr_bottomBorder_col = nAttr.create("Bottom_border_color", "bbc", MFnNumericData::k3Float);
	nAttr.setUsedAsColor(true);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_bottomBorder_col);

	//border height
	attr_border_height = nAttr.create("border_height", "bh", MFnNumericData::kFloat);
	nAttr.setMax(100);
	nAttr.setMin(0);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_border_height);

	//top text 01 enable
	attr_topText_01_cb = nAttr.create("Top_Text_01_enable", "tt_01_enable", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_topText_01_cb);

	//top text 01 showFrame
	attr_topText_01_showFrame = nAttr.create("Top_Text01_showFrame", "tt_01_showFrame", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_topText_01_showFrame);

	//top text01
	MObject	topText = stringFn.create("Top Text 01");
	attr_topText_01 = typedAttr.create("Top_text_01", "tt_01", MFnData::kString);
	typedAttr.setHidden(false);
	typedAttr.setDefault(topText);
	typedAttr.setWritable(true);
	typedAttr.setStorable(true);
	typedAttr.setKeyable(false);
	MPxLocatorNode::addAttribute(attr_topText_01);

	//top text01 width
	attr_topText_01_w = nAttr.create("Top_Text01_w", "ttw_01", MFnNumericData::kFloat);
	nAttr.setWritable(true);
	nAttr.setMin(0.0f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_topText_01_w);

	//top text01 color
	attr_topText_01_color = nAttr.create("Top_Text01_color", "ttcol_01", MFnNumericData::k3Float);
	nAttr.setWritable(true);
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(0.5f, 0.5f, 0.5f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_topText_01_color);

	//top text 02 enable
	attr_topText_02_cb = nAttr.create("Top_Text_02_enable", "tt_02_enable", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_topText_02_cb);
	//top text 02 showFrame
	attr_topText_02_showFrame = nAttr.create("Top_Text02_showFrame", "tt_02_showFrame", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_topText_02_showFrame);

	//top text02
	MObject	topText_02 = stringFn.create("Top Text 02");
	attr_topText_02 = typedAttr.create("Top_text_02", "tt_02", MFnData::kString);
	typedAttr.setHidden(false);
	typedAttr.setDefault(topText_02);
	typedAttr.setWritable(true);
	typedAttr.setStorable(true);
	typedAttr.setKeyable(false);
	MPxLocatorNode::addAttribute(attr_topText_02);

	//top text02 width
	attr_topText_02_w = nAttr.create("Top_Text_02_w", "ttw_02", MFnNumericData::kFloat);
	nAttr.setWritable(true);
	nAttr.setMin(0.0f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_topText_02_w);

	//top text02 color
	attr_topText_02_color = nAttr.create("Top_Text02_color", "ttcol_02", MFnNumericData::k3Float);
	nAttr.setWritable(true);
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(0.5f, 0.5f, 0.5f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_topText_02_color);

	//top text 03 enable
	attr_topText_03_cb = nAttr.create("Top_Text_03_enable", "tt_03_enable", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_topText_03_cb);

	//top text 03 showFrame
	attr_topText_03_showFrame = nAttr.create("Top_Text03_showFrame", "tt_03_showFrame", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_topText_03_showFrame);

	//top text03
	MObject	topText_03 = stringFn.create("Top Text 03");
	attr_topText_03 = typedAttr.create("Top_text_03", "tt_03", MFnData::kString);
	typedAttr.setHidden(false);
	typedAttr.setDefault(topText_03);
	typedAttr.setWritable(true);
	typedAttr.setStorable(true);
	typedAttr.setKeyable(false);
	MPxLocatorNode::addAttribute(attr_topText_03);

	//top text03 width
	attr_topText_03_w = nAttr.create("Top_Text_03_w", "ttw_03", MFnNumericData::kFloat);
	nAttr.setWritable(true);
	nAttr.setMin(0.0f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_topText_03_w);

	//top text03 color
	attr_topText_03_color = nAttr.create("Top_Text03_color", "ttcol_03", MFnNumericData::k3Float);
	nAttr.setWritable(true);
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(0.5f, 0.5f, 0.5f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_topText_03_color);

	//bottom text 01 enable
	attr_bottomText_01_cb = nAttr.create("Bottom_Text01_enable", "bt_01_enable", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_01_cb);

	//bottom text 01 showFrame
	attr_bottomText_01_showFrame = nAttr.create("Bottom_Text01_showFrame", "bt_01_showFrame", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_01_showFrame);

	//bottom text01
	MObject	bottomText_01_string = stringFn.create("Bottom Text 01");
	attr_bottomText_01 = typedAttr.create("Bottom_Text01", "bt_01", MFnData::kString);
	typedAttr.setHidden(false);
	typedAttr.setDefault(bottomText_01_string);
	typedAttr.setWritable(true);
	typedAttr.setStorable(true);
	typedAttr.setKeyable(false);
	MPxLocatorNode::addAttribute(attr_bottomText_01);

	//bottom text01 width
	attr_bottomText_01_w = nAttr.create("Bottom_Text01_w", "btw_01", MFnNumericData::kFloat);
	nAttr.setWritable(true);
	nAttr.setMin(0.0f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_01_w);

	//bottom text01 color
	attr_bottomText_01_color = nAttr.create("Bottom_Text01_color", "btcol_01", MFnNumericData::k3Float);
	nAttr.setWritable(true);
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(0.5f, 0.5f, 0.5f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_01_color);

	//bottom text 02 enable
	attr_bottomText_02_cb = nAttr.create("Bottom_Text02_enable", "bt_02_enable", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_02_cb);

	//bottom text 02 showFrame
	attr_bottomText_02_showFrame = nAttr.create("Bottom_Text02_showFrame", "bt_02_showFrame", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_02_showFrame);

	//bottom text02
	MObject	bottomText_02_string = stringFn.create("Bottom Text 02");
	attr_bottomText_02 = typedAttr.create("Bottom_Text02", "bt_02", MFnData::kString);
	typedAttr.setHidden(false);
	typedAttr.setDefault(bottomText_02_string);
	typedAttr.setWritable(true);
	typedAttr.setStorable(true);
	typedAttr.setKeyable(false);
	MPxLocatorNode::addAttribute(attr_bottomText_02);

	//bottom text02 width
	attr_bottomText_02_w = nAttr.create("Bottom_Text02_w", "btw_02", MFnNumericData::kFloat);
	nAttr.setWritable(true);
	nAttr.setMin(0.0f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_02_w);

	//bottom text02 color
	attr_bottomText_02_color = nAttr.create("Bottom_Text02_color", "btcol_02", MFnNumericData::k3Float);
	nAttr.setWritable(true);
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(0.5f, 0.5f, 0.5f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_02_color);

	//bottom text 03 enable
	attr_bottomText_03_cb = nAttr.create("Bottom_Text03_enable", "bt_03_enable", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_03_cb);

	//bottom text 03 showFrame
	attr_bottomText_03_showFrame = nAttr.create("Bottom_Text03_showFrame", "bt_03_showFrame", MFnNumericData::kBoolean);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_03_showFrame);

	//bottom text03
	MObject	bottomText_03_string = stringFn.create("Bottom Text 03");
	attr_bottomText_03 = typedAttr.create("Bottom_Text03", "bt_03", MFnData::kString);
	typedAttr.setHidden(false);
	typedAttr.setDefault(bottomText_03_string);
	typedAttr.setWritable(true);
	typedAttr.setStorable(true);
	typedAttr.setKeyable(false);
	MPxLocatorNode::addAttribute(attr_bottomText_03);

	//bottom text03 width
	attr_bottomText_03_w = nAttr.create("Bottom_Text03_w", "btw_03", MFnNumericData::kFloat);
	nAttr.setWritable(true);
	nAttr.setMin(0.0f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_03_w);

	//bottom text03 color
	attr_bottomText_03_color = nAttr.create("Bottom_Text03_color", "btcol_03", MFnNumericData::k3Float);
	nAttr.setWritable(true);
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(0.5f, 0.5f, 0.5f);
	nAttr.setStorable(true);
	nAttr.setKeyable(true);
	MPxLocatorNode::addAttribute(attr_bottomText_03_color);

	//test
	MObject	defaultText = stringFn.create("persp");
	attr_camera = typedAttr.create("Camera_ssset", "c___ssssss", MFnData::kString);
	typedAttr.setHidden(false);
	typedAttr.setDefault(defaultText);
	typedAttr.setWritable(true);
	typedAttr.setStorable(true);
	typedAttr.setKeyable(false);
	MPxLocatorNode::addAttribute(attr_camera);


	// size of h
	attr_sizeOfH = nAttr.create("Resolution_Height", "h", MFnNumericData::kFloat, 360.0f);
	nAttr.setKeyable(false);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_sizeOfH);


	//size of w
	attr_sizeOfW = nAttr.create("Resolition_Width", "w", MFnNumericData::kFloat, 640.0f);
	nAttr.setKeyable(false);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_sizeOfW);

	//Frame
	attr_Frame = nAttr.create("Frame", "f", MFnNumericData::kFloat, 0.0f);
	nAttr.setKeyable(false);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	MPxLocatorNode::addAttribute(attr_Frame);

	//transparency
	attr_transparency = nAttr.create("Transparency", "t", MFnNumericData::kDouble, 0.0);
	nAttr.setKeyable(true);
	nAttr.setWritable(true);
	nAttr.setStorable(true);
	nAttr.setMin(0);
	nAttr.setMax(1);
	MPxLocatorNode::addAttribute(attr_transparency);

	return MS::kSuccess;
}



pbDrawManagerData::pbDrawManagerData() : MUserData(false)
		,sCameraName("persp")
		,sTransparency(0.0f)
		,sSizeOfH(360.0f)
		,sSizeOfW(640.0f)
		,sFrame(0.0f)
		,sScratchablelatex(true)
{
}


pbDrawManagerData::~pbDrawManagerData()
{

}

MHWRender::MPxDrawOverride* pbDrawManagerDrawOverride::Creator(const MObject& obj)
{
	return new pbDrawManagerDrawOverride(obj);
}


pbDrawManagerDrawOverride::pbDrawManagerDrawOverride(const MObject &obj)
	: MPxDrawOverride(obj, NULL)
{
}

pbDrawManagerDrawOverride::~pbDrawManagerDrawOverride()
{
}

MHWRender::DrawAPI pbDrawManagerDrawOverride::supportedDrawAPIs() const
{
	return (MHWRender::kOpenGL | MHWRender::kDirectX11 | MHWRender::kOpenGLCoreProfile);
}

bool pbDrawManagerDrawOverride::isBounded(const MDagPath &objPath, const MDagPath &cameraPath) const
{
	return false;
}

MBoundingBox	pbDrawManagerDrawOverride::boundingBox(const MDagPath &objPath, const MDagPath &cameraPath) const
{
	return MBoundingBox();
}

bool		pbDrawManagerDrawOverride::hasUIDrawables() const
{
	return true;
}



//
//preparefordraw
//
//
MUserData*	pbDrawManagerDrawOverride::prepareForDraw(const MDagPath &objPath, const MDagPath &cameraPath, const MHWRender::MFrameContext &frameContext, MUserData *oldData)
{
	pbDrawManagerData* data = dynamic_cast<pbDrawManagerData*>(oldData);
	if (!data)
	{
		data = new pbDrawManagerData();
	}
	MStatus status;
	MObject pbDrawManagerNode = objPath.node(&status);
	if (status)
	{

		//MGlobal::displayInfo("draw!!!!!!!!!!!!!!!!!!!!!!!!!!");
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_transparency);
			data->sTransparency = plug.asFloat();
			MPlug plug_cam(pbDrawManagerNode, pbDrawManager::attr_camera);
			data->sCameraName = plug_cam.asString();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_sizeOfW);
			data->sSizeOfW = plug.asFloat();
		}

		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_sizeOfH);
			data->sSizeOfH = plug.asFloat();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_Frame);
			data->sFrame = plug.asFloat();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_Scratchablelatex);
			data->sScratchablelatex = plug.asBool();
		}

		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topBorder_cb);
			data->sTopBorder_cb = plug.asBool();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomBorder_cb);
			data->sBottomBorder_cb = plug.asBool();
		}

		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_Scratchablelatex_color);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->sSs_color.r, data->sSs_color.g, data->sSs_color.b);
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_border_height);
			data->sBorder_height = plug.asFloat();
		}

		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_topBorder_col);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->stb_color.r, data->stb_color.g, data->stb_color.b);
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomBorder_col);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->sbb_color.r, data->sbb_color.g, data->sbb_color.b);
		}

		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_01);
			data->sTopText01 = plug.asString();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_01_cb);
			data->sTopText01_cb = plug.asBool();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_02);
			data->sTopText02 = plug.asString();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_02_cb);
			data->sTopText02_cb = plug.asBool();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_topText_03);
			data->sTopText03 = plug.asString();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_topText_03_cb);
			data->sTopText03_cb = plug.asBool();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_01_w);
			data->sTopText01_w = plug.asFloat();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_02_w);
			data->sTopText02_w = plug.asFloat();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_03_w);
			data->sTopText03_w = plug.asFloat();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_topText_01_color);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->sTopText01_color.r, data->sTopText01_color.g, data->sTopText01_color.b);
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_topText_02_color);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->sTopText02_color.r, data->sTopText02_color.g, data->sTopText02_color.b);
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_topText_03_color);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->sTopText03_color.r, data->sTopText03_color.g, data->sTopText03_color.b);
		}

		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_01);
			data->sBottomText01 = plug.asString();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_02);
			data->sBottomText02 = plug.asString();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_03);
			data->sBottomText03 = plug.asString();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_01_cb);
			data->sBottomText01_cb = plug.asBool();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_02_cb);
			data->sBottomText02_cb = plug.asBool();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_03_cb);
			data->sBottomText03_cb = plug.asBool();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_01_w);
			data->sBottomText01_w = plug.asFloat();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_02_w);
			data->sBottomText02_w = plug.asFloat();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_03_w);
			data->sBottomText03_w = plug.asFloat();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_01_color);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->sBottomText01_color.r, data->sBottomText01_color.g, data->sBottomText01_color.b);
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_02_color);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->sBottomText02_color.r, data->sBottomText02_color.g, data->sBottomText02_color.b);
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_03_color);
			MObject o = plug.asMObject();
			MFnNumericData nData(o);
			nData.getData(data->sBottomText03_color.r, data->sBottomText03_color.g, data->sBottomText03_color.b);
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_01_showFrame);
			data->sBottomText01_showFrame = plug.asBool();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_02_showFrame);
			data->sBottomText02_showFrame = plug.asBool();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_bottomText_03_showFrame);
			data->sBottomText03_showFrame = plug.asBool();
		}
		{
			MPlug	plug(pbDrawManagerNode, pbDrawManager::attr_topText_01_showFrame);
			data->sTopText01_showFrame = plug.asBool();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_02_showFrame);
			data->sTopText02_showFrame = plug.asBool();
		}
		{
			MPlug plug(pbDrawManagerNode, pbDrawManager::attr_topText_03_showFrame);
			data->sTopText03_showFrame = plug.asBool();

		}
	}
	return data;
}

void	pbDrawManagerDrawOverride::addUIDrawables(const MDagPath &objPath, MHWRender::MUIDrawManager &drawManager, const MHWRender::MFrameContext &frameContext, const MUserData *data)
{
	const pbDrawManagerData* thisdata = dynamic_cast<const pbDrawManagerData*>(data);
	if (!thisdata)
	{
		return;
	}
	drawManager.beginDrawable();
	int x, y, w, h;
	frameContext.getViewportDimensions(x, y, w, h);
	int borderSize[] = {thisdata->sSizeOfW, thisdata->sBorder_height};
	MTime		currentFrame = MAnimControl::currentTime();
	double		currentFrame_dd = currentFrame.value();
	MString	frameData;
	frameData += "Frame:";
	frameData += currentFrame_dd;
	if (thisdata->sScratchablelatex)
	{
		drawManager.setColor(MColor(thisdata->sSs_color.r, thisdata->sSs_color.g, thisdata->sSs_color.b, thisdata->sTransparency));
		//h1
		drawManager.line2d(MPoint(w / 2 - (thisdata->sSizeOfW / 6 + thisdata->sSizeOfW / 3), h / 2 - thisdata->sSizeOfH/6), 
										  MPoint(w / 2 + (thisdata->sSizeOfW / 6 + thisdata->sSizeOfW / 3), h / 2 - thisdata->sSizeOfH / 6));
		//h2
		drawManager.line2d(MPoint(w / 2 - (thisdata->sSizeOfW / 3 + thisdata->sSizeOfW / 6), h / 2 + thisdata->sSizeOfH / 6),
										  MPoint(w / 2 + (thisdata->sSizeOfW / 3 + thisdata->sSizeOfW / 6), h / 2 + thisdata->sSizeOfH / 6));
		//v1
		drawManager.line2d(MPoint(w / 2 - thisdata->sSizeOfW / 6 , h / 2 - (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3)),
										  MPoint(w / 2 - thisdata->sSizeOfW / 6 , h / 2 + (thisdata->sSizeOfH / 6 +thisdata->sSizeOfH/3)));
		//v2 
		drawManager.line2d(MPoint(w / 2 + thisdata->sSizeOfW / 6, h / 2 - (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3)),
										  MPoint(w / 2 + thisdata->sSizeOfW / 6, h / 2 + (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3)));

	} 
	if (thisdata->sTopBorder_cb)
	{

		drawManager.text2d(MPoint(w/2, h / 2 + (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3)-thisdata->sBorder_height), MString("  "), MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(thisdata->stb_color.r, thisdata->stb_color.g, thisdata->stb_color.b, thisdata->sTransparency));
	}
	if (thisdata->sBottomBorder_cb)
	{
		drawManager.text2d(MPoint(w/2, h / 2 - (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3) ), MString("  "), MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(thisdata->sbb_color.r, thisdata->sbb_color.g, thisdata->sbb_color.b, thisdata->sTransparency));
	}
	if (thisdata->sTopText01_cb)
	{
		drawManager.setColor(MColor(thisdata->sTopText01_color.r, thisdata->sTopText01_color.g, thisdata->sTopText01_color.b, thisdata->sTransparency));
		if (thisdata->sTopText01_showFrame)
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sTopText01_w, h / 2 + (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3) - thisdata->sBorder_height), frameData, MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
		else 
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sTopText01_w, h / 2 + (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3) - thisdata->sBorder_height), MString(thisdata->sTopText01), MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
	}
	if (thisdata->sTopText02_cb)
	{
		drawManager.setColor(MColor(thisdata->sTopText02_color.r, thisdata->sTopText02_color.g, thisdata->sTopText02_color.b, thisdata->sTransparency));
		if (thisdata->sTopText02_showFrame)
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sTopText02_w, h / 2 + (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3) - thisdata->sBorder_height), frameData, MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
		else
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sTopText02_w, h / 2 + (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3) - thisdata->sBorder_height), MString(thisdata->sTopText02), MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
	}
	if (thisdata->sTopText03_cb)
	{
		drawManager.setColor(MColor(thisdata->sTopText03_color.r, thisdata->sTopText03_color.g, thisdata->sTopText03_color.b, thisdata->sTransparency));
		if (thisdata->sTopText03_showFrame)
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sTopText03_w, h / 2 + (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3) - thisdata->sBorder_height), frameData, MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));

		}
		else
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sTopText03_w, h / 2 + (thisdata->sSizeOfH / 6 + thisdata->sSizeOfH / 3) - thisdata->sBorder_height), MString(thisdata->sTopText03), MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
	}
	if (thisdata->sBottomText01_cb)
	{
		drawManager.setColor(MColor(thisdata->sBottomText01_color.r, thisdata->sBottomText01_color.g, thisdata->sBottomText01_color.b, thisdata->sTransparency));
		if (thisdata->sBottomText01_showFrame)
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sBottomText01_w, h / 2 - thisdata->sSizeOfH / 2), frameData, MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
		else
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sBottomText01_w, h / 2 - thisdata->sSizeOfH / 2), MString(thisdata->sBottomText01), MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
	}
	if (thisdata->sBottomText02_cb)
	{
		drawManager.setColor(MColor(thisdata->sBottomText02_color.r, thisdata->sBottomText02_color.g, thisdata->sBottomText02_color.b, thisdata->sTransparency));
		if (thisdata->sBottomText02_showFrame)
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sBottomText02_w, h / 2 - thisdata->sSizeOfH / 2), frameData, MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));

		}
		else
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sBottomText02_w, h / 2 - thisdata->sSizeOfH / 2), MString(thisdata->sBottomText02), MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
	}
	if (thisdata->sBottomText03_cb)
	{
		drawManager.setColor(MColor(thisdata->sBottomText03_color.r, thisdata->sBottomText03_color.g, thisdata->sBottomText03_color.b, thisdata->sTransparency));
		if (thisdata->sBottomText03_showFrame)
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sBottomText03_w, h / 2 - thisdata->sSizeOfH / 2), frameData, MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));

		}
		else
		{
			drawManager.text2d(MPoint(w / 2 - thisdata->sSizeOfW / 2 + thisdata->sBottomText03_w, h / 2 - thisdata->sSizeOfH / 2), MString(thisdata->sBottomText03), MHWRender::MUIDrawManager::kCenter, borderSize, &MColor(0.0f, 0.0f, 0.0f, 0.0f));
		}
	}






	drawManager.endDrawable();


	

}


MStatus initializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj, PLUGIN_COMPANY, "3.0", "Any");

	status = plugin.registerNode(
		"pbDrawManager",
		pbDrawManager::id,
		&pbDrawManager::creator,
		&pbDrawManager::initialize,
		MPxNode::kLocatorNode,
		&pbDrawManager::drawDbClassification);
	if (!status) {
		status.perror("registerNode");
		return status;
	}

	status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
		pbDrawManager::drawDbClassification,
		pbDrawManager::drawRegistrantId,
		pbDrawManagerDrawOverride::Creator);
	if (!status) {
		status.perror("registerDrawOverrideCreator");
		return status;
	}

	return status;
}

MStatus uninitializePlugin(MObject obj)
{
	MStatus   status;
	MFnPlugin plugin(obj);

	status = MHWRender::MDrawRegistry::deregisterGeometryOverrideCreator(
		pbDrawManager::drawDbClassification,
		pbDrawManager::drawRegistrantId);
	if (!status) {
		status.perror("deregisterGeometryOverrideCreator");
		return status;
	}

	status = plugin.deregisterNode(pbDrawManager::id);
	if (!status) {
		status.perror("deregisterNode");
		return status;
	}

	return status;
}
