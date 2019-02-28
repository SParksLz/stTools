#ifndef viewOverrideSimple_h_
#define viewOverrideSimple_h_
//-
// Copyright 2015 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license agreement
// provided at the time of installation or download, or which otherwise
// accompanies this software in either electronic or hard copy form.
//+
#include <maya/MString.h>
#include <maya/MStatus.h>
#include <maya/MPxCommand.h>
#include <maya/MViewport2Renderer.h>
#include <maya/MFnPlugin.h>
#include <maya/MArgDatabase.h>
#include <maya/MSyntax.h>
#include <stdio.h>


#define kSetHeightFlag			"-sh"
#define kSetHeightFlagLong	"-setheight"	
#define kSetWidthFlag			"-sw"
#define kSetWidthFlagLong	"-setwidth"
#define kSetHudDisplay			"-hd"
#define kSetHudDisplayLong	"-huddisplay"




double r_height = 720;
double r_width = 1280;
bool displayOperation = true;
//
// Simple override class derived from MRenderOverride
//
class viewOverrideSimple : public MHWRender::MRenderOverride
{
public:
	viewOverrideSimple(const MString & name);
	virtual ~viewOverrideSimple();
	virtual MHWRender::DrawAPI supportedDrawAPIs() const;

	// Basic setup and cleanup
	virtual MStatus setup(const MString & destination);
	virtual MStatus cleanup();

	// Operation iteration methods
	virtual bool startOperationIterator();
	virtual MHWRender::MRenderOperation * renderOperation();
	virtual bool nextRenderOperation();

	// UI name
	virtual MString uiName() const
	{
		return mUIName;
	}

protected:
	// UI name 
	MString mUIName;

	// Operations and operation names
	MHWRender::MRenderOperation* mOperations[3];
	MString mOperationNames[3];

	// Temporary of operation iteration
	int mCurrentOperation;
};

//
// Simple scene operation override to allow for clear color
// tracking.
//
class simpleViewRenderSceneRender : public MHWRender::MSceneRender
{
public:
	simpleViewRenderSceneRender(const MString &name);
	virtual MHWRender::MClearOperation & clearOperation();
};



class simpleHUDOperation : public MHWRender::MHUDRender
{
public : 
	simpleHUDOperation()
	{

		mTargets = NULL;
	}
	virtual MHWRender::MRenderTarget* const* targetOverrideList(unsigned int &listSize) {
		if (mTargets)
		{
			listSize = 2;
			return &mTargets[0];
		}
		listSize = 0;
		return NULL;
	}
	virtual bool hasUIDrawables() const { return true; }
	virtual void addUIDrawables(MHWRender::MUIDrawManager& drawManager2D, const MHWRender::MFrameContext& frameContext);
	void setRenderTargets(MHWRender::MRenderTarget **targets) { mTargets = targets; }
	~simpleHUDOperation() {
		mTargets = NULL;
	}


	//double r_height=720;
	//double r_width=1280;

protected :  
	MHWRender::MRenderTarget**  mTargets;

};

class hudController : public MPxCommand
{
public :  
	hudController() {}
	virtual ~hudController() {}
	static MSyntax	  newSyntax();
	static void*	creator() { return new hudController; }
	virtual MStatus doIt(const MArgList &args);
	virtual bool isundoable() { return true; }
	//void setRHeight(double *height);
	//void setRwidth(double *width);
};






#endif


