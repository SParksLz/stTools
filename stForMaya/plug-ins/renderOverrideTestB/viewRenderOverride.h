//
// Created by dirty on 2019/2/13.
//

#ifndef RENDEROVERRIDETESTB_VIEWRENDEROVERRIDE_H
#define RENDEROVERRIDETESTB_VIEWRENDEROVERRIDE_H

#endif //RENDEROVERRIDETESTB_VIEWRENDEROVERRIDE_H
#include <maya/MString.h>
#include <maya/MStatus.h>
#include <maya/MUIDrawManager.h>
#include <maya/MViewport2Renderer.h>
#include <maya/MFrameContext.h>
#include <maya/M3dView.h>


class viewRenderOverride : public MHWRender::MRenderOverride
{
public :
    viewRenderOverride(const MString &name);

    virtual								~viewRenderOverride();
    virtual MHWRender::DrawAPI			supportedDrawAPIs() const;
    virtual bool						startOperationIterator();
    virtual MHWRender::MRenderOperation *renderOperation();
    virtual bool						nextRenderOperation();
    virtual MStatus						setup( const MString & destination );
    virtual MStatus						cleanup();
    virtual MString						uiName() const
    {
        return mUIName;
    }
protected:
    MString								mUIName;
    int									mCurrentOperation;
    MHWRender::MRenderOperation*		mOperations[1];
    MString								mOperationNames[3];


};

class viewHUDRenderOp : public MHWRender::MHUDRender
{
public:
    viewHUDRenderOp();
    virtual bool								hasUIDrawables() const;
    virtual void								addUIDrawables( MHWRender::MUIDrawManager &drawManager2D,const MHWRender::MFrameContext &frameContext);
    virtual MHWRender::MRenderTarget* const*	targetOverrideList(unsigned int &listSize);
    void setRenderTargets(MHWRender::MRenderTarget **targets)
    {
        mTargets = targets;
    }

    ~viewHUDRenderOp()
    {
        mTargets = NULL;
    }
    double								resolutionHeight, resolutionWidth;
protected:
    MHWRender::MRenderTarget** mTargets;
    //double								resolutionHeight, resolutionWidth;



};