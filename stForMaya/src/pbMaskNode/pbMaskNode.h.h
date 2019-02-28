#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

#include <maya/MPxDrawOverride.h>
#include <maya/MPxLocatorNode.h>
#include <maya/MFrameContext.h>
#include <maya/MUIDrawManager.h>
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnStringData.h>
#include <maya/MFnPlugin.h>
#include <maya/MDrawRegistry.h>
#include <maya/MStatus.h>
#include <maya/MFnDagNode.h>
#include <maya/MGlobal.h>
#include <maya/MFnData.h>
#include <maya/MTime.h>
#include <maya/MAnimControl.h>




class pbDrawManager : public MPxLocatorNode
{
public : 
								pbDrawManager();
	virtual					~pbDrawManager();
	static	void*		creator() { return new pbDrawManager(); }
	static	MStatus	initialize();
	static	MTypeId	id;
	//attribute
	static	MObject	attr_transparency;
	static	MObject	attr_Frame;
	static	MObject	attr_sizeOfW;
	static	MObject	attr_sizeOfH;
	static	MObject	attr_camera;
	static	MObject	attr_Scratchablelatex;
	static	MObject	attr_Scratchablelatex_color;
	static	MObject	attr_topBorder_cb;
	static	MObject	attr_topBorder_col;
	static	MObject	attr_bottomBorder_cb;
	static	MObject	attr_bottomBorder_col;
	static	MObject	attr_border_height;


	static	MObject	attr_topText_01;
	static	MObject	attr_topText_01_cb;
	static	MObject	attr_topText_01_w;
	static	MObject	attr_topText_01_color;
	static	MObject	attr_topText_01_showFrame;
	static	MObject	attr_topText_02;
	static	MObject	attr_topText_02_cb;
	static	MObject	attr_topText_02_w;
	static	MObject	attr_topText_02_color;
	static	MObject	attr_topText_02_showFrame;
	static	MObject	attr_topText_03;
	static	MObject	attr_topText_03_cb;
	static	MObject	attr_topText_03_w;
	static	MObject	attr_topText_03_color;
	static	MObject	attr_topText_03_showFrame;

	static	MObject	attr_bottomText_01;
	static	MObject	attr_bottomText_01_cb;
	static	MObject	attr_bottomText_01_w;
	static	MObject	attr_bottomText_01_color;
	static	MObject	attr_bottomText_01_showFrame;
	static	MObject	attr_bottomText_02;
	static	MObject	attr_bottomText_02_cb;
	static	MObject	attr_bottomText_02_w;
	static	MObject	attr_bottomText_02_color;
	static	MObject	attr_bottomText_02_showFrame;

	static	MObject	attr_bottomText_03;
	static	MObject	attr_bottomText_03_cb;
	static	MObject	attr_bottomText_03_w;
	static	MObject	attr_bottomText_03_color;
	static	MObject	attr_bottomText_03_showFrame;


	static	MString	drawDbClassification;
	static	MString	drawRegistrantId;
};

class pbDrawManagerData : public MUserData
{
public:
								pbDrawManagerData();
	virtual					~pbDrawManagerData();
	MString				sCameraName;

	int						sTopText_size;

	MString				sTopText01;
	bool						sTopText01_cb;
	float						sTopText01_w;
	MColor				sTopText01_color;
	bool						sTopText01_showFrame;

	MString				sTopText02;
	bool						sTopText02_cb;
	float						sTopText02_w;
	MColor				sTopText02_color;
	bool						sTopText02_showFrame;

	MString				sTopText03;
	bool						sTopText03_cb;
	float						sTopText03_w;
	MColor				sTopText03_color;
	bool						sTopText03_showFrame;
	
	MString				sBottomText01;
	bool						sBottomText01_cb;
	float						sBottomText01_w;
	MColor				sBottomText01_color;
	bool						sBottomText01_showFrame;

	MString				sBottomText02;
	bool						sBottomText02_cb;
	float						sBottomText02_w;
	MColor				sBottomText02_color;
	bool						sBottomText02_showFrame;

	MString				sBottomText03;
	bool						sBottomText03_cb;
	float						sBottomText03_w;
	MColor				sBottomText03_color;
	bool						sBottomText03_showFrame;

	MColor				sSs_color;
	MColor				stb_color;
	MColor				sbb_color;
	float						sBorder_height;



	float						sBackground_w;
	float						sBackground_h;

	float						sTopBoreder_pos;
	float						sBottomBoreder_pos;


	float						sTransparency;
	float						sSizeOfW;
	float						sSizeOfH;
	float						sFrame;

	//float						sbbHeight;
	//float						stbHeight;

	bool						sTopBorder_cb;
	bool						sBottomBorder_cb;



	bool						sScratchablelatex;

};


class pbDrawManagerDrawOverride : public MHWRender::MPxDrawOverride
{
public : 
	static	MHWRender::MPxDrawOverride*				Creator(const MObject& obj);
	virtual												~pbDrawManagerDrawOverride();
	virtual	MHWRender::DrawAPI		supportedDrawAPIs() const;
	virtual	bool										hasUIDrawables() const;
	virtual MUserData *							prepareForDraw(const MDagPath &objPath, const MDagPath &cameraPath, const MHWRender::MFrameContext &frameContext, MUserData *oldData);
	virtual void										addUIDrawables(const MDagPath &objPath, MHWRender::MUIDrawManager &drawManager, const MHWRender::MFrameContext &frameContext, const MUserData *data);
	virtual MBoundingBox					boundingBox(const MDagPath &objPath, const MDagPath &cameraPath) const;
	virtual bool										isBounded(const MDagPath &objPath, const MDagPath &cameraPath) const;
	//void													drawLine(MHWRender::MUIDrawManager &draw_manager);
private : 
															pbDrawManagerDrawOverride(const MObject &obj);

};

