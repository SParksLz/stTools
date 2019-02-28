//-
// Copyright 2015 Autodesk, Inc.  All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license agreement
// provided at the time of installation or download, or which otherwise
// accompanies this software in either electronic or hard copy form.
//+
#include "renderOverrideview.h"


// For override creation we return a UI name so that it shows up in as a
// renderer in the 3d viewport menus.
// 
viewOverrideSimple::viewOverrideSimple(const MString & name)
	: MRenderOverride(name)
	, mUIName("Simple VP2 Override")
	, mCurrentOperation(-1)
{
	mOperations[0] = mOperations[1] = mOperations[2] = NULL;
	mOperationNames[0] = "viewOverrideSimple_Scene";
	mOperationNames[1] = "viewOverrideSimple_HUD";
	mOperationNames[2] = "viewOverrideSimple_Present";

}

// On destruction all operations are deleted.
//
viewOverrideSimple::~viewOverrideSimple()
{
	for (unsigned int i = 0; i < 3; i++)
	{
		if (mOperations[i])
		{
			delete mOperations[i];
			mOperations[i] = NULL;
		}
	}
}

// Drawing uses all internal code so will support all draw APIs
//
MHWRender::DrawAPI viewOverrideSimple::supportedDrawAPIs() const
{
	return MHWRender::kAllDevices;
}

// Basic iterator methods which returns a list of operations in order
// The operations are not executed at this time only queued for execution
//
// - startOperationIterator() : to start iterating
// - renderOperation() : will be called to return the current operation
// - nextRenderOperation() : when this returns false we've returned all operations
//
bool viewOverrideSimple::startOperationIterator()
{
	mCurrentOperation = 0;
	return true;
}

MHWRender::MRenderOperation*
viewOverrideSimple::renderOperation()
{
	if (mCurrentOperation >= 0 && mCurrentOperation < 3)
	{
		if (mOperations[mCurrentOperation])
		{
			return mOperations[mCurrentOperation];
		}
	}
	return NULL;
}

bool
viewOverrideSimple::nextRenderOperation()
{
	mCurrentOperation++;
	if (mCurrentOperation < 3)
	{
		return true;
	}
	return false;
}

//
// On setup we make sure that we have created the appropriate operations
// These will be returned via the iteration code above.
//
// The only thing that is required here is to create:
//
//	- One scene render operation to draw the scene.
//	- One "stock" HUD render operation to draw the HUD over the scene
//	- One "stock" presentation operation to be able to see the results in the viewport
//
MStatus viewOverrideSimple::setup(const MString & destination)
{
	MHWRender::MRenderer *theRenderer = MHWRender::MRenderer::theRenderer();
	if (!theRenderer)
		return MStatus::kFailure;

	// Create a new set of operations as required
	if (!mOperations[0])
	{
		mOperations[0] = (MHWRender::MRenderOperation *) new simpleViewRenderSceneRender(mOperationNames[0]);
		mOperations[1] = new  simpleHUDOperation();
		mOperations[2] = (MHWRender::MRenderOperation *) new MHWRender::MPresentTarget(mOperationNames[2]);
	}
	if (!mOperations[0] ||
		!mOperations[1] ||
		!mOperations[2])
	{
		return MStatus::kFailure;
	}

	return MStatus::kSuccess;
}

// On cleanup we just return for returning the list of operations for
// the next render
//
MStatus viewOverrideSimple::cleanup()
{
	mCurrentOperation = -1;
	return MStatus::kSuccess;
}

// The only customization for the scene render (and hence derivation)
// is to be able to set the background color.
//
simpleViewRenderSceneRender::simpleViewRenderSceneRender(const MString &name)
	: MSceneRender(name)
{
}


void simpleHUDOperation::addUIDrawables(MHWRender::MUIDrawManager& drawManager2D, const MHWRender::MFrameContext& frameContext)
{
	float resolutionH, resolutionW;
	resolutionH = r_height;
	resolutionW = r_width;

	
	drawManager2D.beginDrawable();
	if (displayOperation)
	{
		drawManager2D.setColor(MColor(0.455f, 0.212f, 0.596f));
		drawManager2D.setFontSize(MHWRender::MUIDrawManager::kSmallFontSize);
		int x = 0, y = 0, w = 0, h = 0;
		frameContext.getViewportDimensions(x, y, w, h);
		drawManager2D.line2d(MPoint(0, h / 2 - resolutionH / 6), MPoint(w, h / 2 - resolutionH / 6));
		drawManager2D.line2d(MPoint(0, h / 2 + resolutionH / 6), MPoint(w, h / 2 + resolutionH / 6));
		drawManager2D.line2d(MPoint(w / 2 - resolutionW / 6, 0), MPoint(w / 2 - resolutionW / 6, h));
		drawManager2D.line2d(MPoint(w / 2 + resolutionW / 6, 0), MPoint(w / 2 + resolutionW / 6, h));
		drawManager2D.text2d( MPoint(w / 2, h / 2), MString("Center") );
	}
	drawManager2D.endDrawable();

}



// Background color override. We get the current colors from the 
// renderer and use them
//
MHWRender::MClearOperation &
simpleViewRenderSceneRender::clearOperation()
{
	MHWRender::MRenderer* renderer = MHWRender::MRenderer::theRenderer();
	bool gradient = renderer->useGradient();
	MColor color1 = renderer->clearColor();
	MColor color2 = renderer->clearColor2();

	float c1[4] = { color1[0], color1[1], color1[2], 1.0f };
	float c2[4] = { color2[0], color2[1], color2[2], 1.0f };

	mClearOperation.setClearColor(c1);
	mClearOperation.setClearColor2(c2);
	mClearOperation.setClearGradient(gradient);
	return mClearOperation;
}


MSyntax hudController::newSyntax()
{
	MSyntax syntax;
	syntax.addFlag(kSetHeightFlag, kSetHeightFlagLong, MSyntax::kDouble);
	syntax.addFlag(kSetWidthFlag, kSetWidthFlagLong, MSyntax::kDouble);
	syntax.addFlag(kSetHudDisplay, kSetHudDisplayLong, MSyntax::kBoolean);
	return syntax;

}


MStatus hudController::doIt(const MArgList &args) {
	MStatus status = MS::kSuccess;
	MArgDatabase argData(syntax(), args);
	if (argData.isFlagSet(kSetHeightFlag))
	{
		double result;
		argData.getFlagArgument(kSetHeightFlag, 0, result);
		r_height = result;

	}
	else if (argData.isFlagSet(kSetWidthFlag))
	{
		double result;
		argData.getFlagArgument(kSetWidthFlag, 0, result);
		r_width = result;
	}
	else if (argData.isFlagSet(kSetWidthFlag))
	{
		bool result;
		argData.getFlagArgument(kSetHudDisplay, 0, result);
		displayOperation = result;
	}
	return MS::kSuccess;
}




MStatus initializePlugin(MObject obj)
{
	MStatus status;
	MFnPlugin plugin(obj, PLUGIN_COMPANY, "1.0", "Any");

	MHWRender::MRenderer* renderer = MHWRender::MRenderer::theRenderer();
	if (renderer)
	{
		// We register with a given name
		viewOverrideSimple *overridePtr = new viewOverrideSimple("viewOverrideSimple");
		if (overridePtr)
		{
			renderer->registerOverride(overridePtr);
		}
	}
	plugin.registerCommand("hudController", hudController::creator, hudController::newSyntax);
	return status;
}



//
// On plug-in de-initialization we deregister a new override
//
MStatus uninitializePlugin(MObject obj)
{
	MStatus status;
	MFnPlugin plugin(obj);

	MHWRender::MRenderer* renderer = MHWRender::MRenderer::theRenderer();
	if (renderer)
	{
		// Find override with the given name and deregister
		const MHWRender::MRenderOverride* overridePtr = renderer->findRenderOverride("viewOverrideSimple");
		if (overridePtr)
		{
			renderer->deregisterOverride(overridePtr);
			delete overridePtr;
		}
	}
	plugin.deregisterCommand("hudController");
	return status;
}
