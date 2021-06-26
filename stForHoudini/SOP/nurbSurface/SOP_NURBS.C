/*
 * Copyright (c) 2020
 *	Side Effects Software Inc.  All rights reserved.
 *
 * Redistribution and use of Houdini Development Kit samples in source and
 * binary forms, with or without modification, are permitted provided that the
 * following conditions are met:
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. The name of Side Effects Software may not be used to endorse or
 *    promote products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY SIDE EFFECTS SOFTWARE `AS IS' AND ANY EXPRESS
 * OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
 * NO EVENT SHALL SIDE EFFECTS SOFTWARE BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
 * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *----------------------------------------------------------------------------
 * The NURBS SOP
 */





#include "SOP_NURBS.h"
#include <GU/GU_Detail.h>
#include <GU/GU_PrimNURBSurf.h>

#include <GA/GA_Types.h>
#include <GA/GA_IndexMap.h>
#include <GA/GA_Primitive.h>

#include <GEO/GEO_PrimPoly.h>
#include <GEO/GEO_PrimType.h>


#include <OP/OP_Operator.h>
#include <OP/OP_OperatorTable.h>
#include <PRM/PRM_Include.h>
#include <UT/UT_DSOVersion.h>
#include <SYS/SYS_Math.h>
#include <limits.h>
#include <stddef.h>
#include <iostream>
#include <vector>

using namespace HDK_Sample;

///
/// newSopOperator is the hook that Houdini grabs from this dll
/// and invokes to register the SOP.  In this case we add ourselves
/// to the specified operator table.
///
void loadFbx(const char * fileName, GU_Detail * gdp);
void i_fbx(FbxNode * node, std::ostringstream & aaa, GU_Detail * gdp);



void
newSopOperator(OP_OperatorTable *table)
{
    table->addOperator(new OP_Operator(
        "hdk_nurbs_test",                    // Internal name
        "XXXX",                        // UI name
        SOP_NURBS::myConstructor,       // How to build the SOP
        SOP_NURBS::myTemplateList,      // My parameters
        0,                              // Min # of sources
        0,                              // Max # of sources
        0,                              // Local variables
        OP_FLAG_GENERATOR));            // Flag it as generator
}
static PRM_Name          theFileName("file", "Load Fbx file");
static PRM_Default       theFileDefault(0, "junk.out");

static int fileName_callBack(void *data, int index, fpreal32 time, const PRM_Template * tplate)
{
	SOP_NURBS * node = (SOP_NURBS *)data;
	UT_String path;
	node->evalString(path, theFileName.getToken(), 0, time);
	if (!path.isstring())
	{
		path = "null";
	}

	if (path != "null")
	{
		std::cout << path << std::endl;
		std::cout << "index : " << index << std::endl;
		std::cout << "-----------------" << std::endl;

	}
	else
	{
		node->addWarning(SOP_VEX_ERROR, "No filename specified. Using null");
	}

	return 0;

}

//parameter µÄ¶¨Òå
PRM_Template
SOP_NURBS::myTemplateList[] = {
	PRM_Template(PRM_INT,			// Integer parameter.
		PRM_Template::PRM_EXPORT_TBX,	// Export to top of viewer
		2, &PRMdivName, PRMfourDefaults),
	PRM_Template(	PRM_INT,
					PRM_Template::PRM_EXPORT_TBX,	// Export to top of viewer
					2, 
					&PRMorderName,
					PRMfourDefaults,
					NULL, 
					&PRMorderRange),
	PRM_Template(	PRM_FILE,
					1, 
					&theFileName, 
					&theFileDefault,
					0,
					0,
					&fileName_callBack,
					0,
					1,
					"helloworld",
					0),
    PRM_Template()
};


OP_Node *
SOP_NURBS::myConstructor(OP_Network *net, const char *name, OP_Operator *op)
{
    return new SOP_NURBS(net, name, op);
}

SOP_NURBS::SOP_NURBS(OP_Network *net, const char *name, OP_Operator *op)
    : SOP_Node(net, name, op)
{
    // This indicates that this SOP manually manages its data IDs,
    // so that Houdini can identify what attributes may have changed,
    // e.g. to reduce work for the viewport, or other SOPs that
    // check whether data IDs have changed.
    // By default, (i.e. if this line weren't here), all data IDs
    // would be bumped after the SOP cook, to indicate that
    // everything might have changed.
    // If some data IDs don't get bumped properly, the viewport
    // may not update, or SOPs that check data IDs
    // may not cook correctly, so be *very* careful!
    mySopFlags.setManagesDataIDs(true);
}

SOP_NURBS::~SOP_NURBS() {}

OP_ERROR
SOP_NURBS::cookMySop(OP_Context &context)
{
    fpreal now = context.getTime();

    //int nu = SYSmax(COLS(now), 2); // Number of columns
    //int nv = SYSmax(ROWS(now), 2); // Number of rows
    //int uorder = SYSmin(UORDER(now), nu);
    //int vorder = SYSmin(VORDER(now), nv);
	UT_String fileName;
	fbxFile(now, fileName);
	//fbxFile(now, fileName);
	std::cout << "1.-fileName is ----> ";
	std::cout << fileName << std::endl;
	if (!fileName.isstring())
	{
		fileName = "null";
		addWarning(SOP_VEX_ERROR, "No filename specified. Using null");
	}
	std::cout << "2.-fileName is ----> ";
	std::cout << fileName << std::endl;

	const char * file_name = fileName;
	gdp->clearAndDestroy();
	loadFbx(file_name, gdp);





    // In addition to destroying everything except the empty P
    // and topology attributes, this bumps the data IDs for
    // those remaining attributes, as well as the primitive list
    // data ID.
    //gdp->clearAndDestroy();

   // // Create a NURBS surface.
   // GEO_PrimNURBSurf *surf = GU_PrimNURBSurf::build(gdp, nv, nu, uorder, vorder);
	

   // /// @see GEO_TPSurf for basis access methods.

   // for (int u = 0; u < nu; u++)
   // {
   //     fpreal s = SYSfit((fpreal)u, u, (fpreal)nu-1, 0, 1);
   //     for (int v = 0; v < nv; v++)
   //     {
   //         fpreal t = SYSfit((fpreal)v, v, (fpreal)nv-1, 0, 1);

   //         UT_Vector4 P(s, 0, t, 1);
   //         GA_Offset ptoff = surf->getPointOffset(v, u); // row, column
   //         gdp->setPos4(ptoff, P);
			//gdp->setDetailAttributeS("pathName", file_name);
   //     }
   // }

   // // We don't need to bump any data IDs here, because they were already
   // // bumped in clearAndDestroy().

    return error();
}



void loadFbx(const char * fileName, GU_Detail * gdpp)
{
	std::cout << "create fbx Manager" << std::endl;
	FbxManager *testManager = FbxManager::Create();
	std::cout << "create fbx io settings" << std::endl;
	FbxIOSettings *ios = FbxIOSettings::Create(testManager, IOSROOT);
	testManager->SetIOSettings(ios);

	std::cout << "create an importer using the sdk manager" << std::endl;
	FbxImporter * testImporter = FbxImporter::Create(testManager, "");
	std::cout << fileName << std::endl;
	bool importerStatus = testImporter->Initialize(fileName, -1, testManager->GetIOSettings());


	if (!importerStatus)
	{
		std::cout << "call to fbxImporter::Initialize() failed " << std::endl;
		std::cout << "Error returned: " << testImporter->GetStatus().GetErrorString() << std::endl;
		//exit(-1);
	}

	else
	{
		FbxScene * testScene = FbxScene::Create(testManager, "myScene");
		int totalNodeCount = testScene->GetNodeCount();
		char ** nodeList = (char **)malloc(sizeof(char) * totalNodeCount);

		testImporter->Import(testScene);

		testImporter->Destroy();
		std::cout << "Destroy importer" << std::endl;
		FbxNode * rootNode = testScene->GetRootNode();
		std::cout << "--------------------start loading-------------------" << std::endl;
		//std::string a = "";
		std::ostringstream aaa;
		i_fbx(rootNode, aaa, gdpp);
		std::cout << "--------------------end loading-------------------";
	}
	//int childCount = rootNode->GetChildCount();
	//for (int i = 0; i < childCount; i++)
	//{
	//	FbxNode * currentNode = rootNode->GetChild(i);

	//}



}
void i_fbx(FbxNode * node, std::ostringstream & aaa, GU_Detail * gdp)
{
	bool hasChild;
	int childCount = node->GetChildCount();
	GA_PrimitiveGroup  * prim_group;
	if (childCount > 0)
	{
		hasChild = true;
	}
	else
	{
		hasChild = false;
	}

	if (hasChild)
	{

		for (int i = 0; i < childCount; i++)
		{

			FbxNode * currentNode = node->GetChild(i);
			FbxNode * parentNode = currentNode->GetParent();

			FbxAMatrix matrix_b =  parentNode->EvaluateGlobalTransform();

			prim_group = gdp->newPrimitiveGroup(currentNode->GetName());
			//std::cout << currentNode->GetName() << std::endl;
			FbxMesh * currentMesh = currentNode->GetMesh();
			if (currentMesh != NULL)
			{
				int v_count = currentMesh->GetPolygonVertexCount();
				int pointCount = currentMesh->GetControlPointsCount();
				int polyCount = currentMesh->GetPolygonCount();


				GA_Offset startptoff = gdp->appendPointBlock(pointCount);




				for (int i = 0; i < pointCount; ++i)
				{
					FbxVector4 p = currentMesh->GetControlPointAt(i);
					p = matrix_b.MultT(p);
					GA_Offset ptoff = startptoff + i;
					gdp->setPos4(ptoff, p[0], p[1], p[2], p[3]);
				}
				for (int i = 0; i < polyCount ; i++)
				{
					int lCount = currentMesh->GetPolygonSize(i);


					if (lCount == 4)
					{
						GEO_PrimPoly *prim_poly_ptr = (GEO_PrimPoly *)gdp->appendPrimitive(GA_PRIMPOLY);
						//GEO_PrimPoly *prim_poly_ptr_2 = (GEO_PrimPoly *)gdp->appendPrimitive(GA_PRIMPOLY);
						GA_Offset prim_start_off = prim_poly_ptr->getVertexOffset(3);
						//GA_Offset prim_start_off_2 = prim_poly_ptr_2->getVertexOffset(3);

						int v0 = currentMesh->GetPolygonVertex(i, 1);
						int v1 = currentMesh->GetPolygonVertex(i, 0);
						int v2 = currentMesh->GetPolygonVertex(i, 3);
						int v3 = currentMesh->GetPolygonVertex(i, 2);

						//int v1_1 = currentMesh->GetPolygonVertex(i, 3);
						//int v1_2 = currentMesh->GetPolygonVertex(i, 2);
						//int v1_3 = currentMesh->GetPolygonVertex(i, 1);

						prim_poly_ptr->appendVertex(startptoff + v0);
						prim_poly_ptr->appendVertex(startptoff + v1);
						prim_poly_ptr->appendVertex(startptoff + v2);
						prim_poly_ptr->appendVertex(startptoff + v3);

						//prim_poly_ptr_2->appendVertex(startptoff + v1_1);
						//prim_poly_ptr_2->appendVertex(startptoff + v1_2);
						//prim_poly_ptr_2->appendVertex(startptoff + v1_3);

						prim_poly_ptr->close();
						//prim_poly_ptr_2->close();
						prim_group->add(prim_poly_ptr);
						//prim_group->add(prim_poly_ptr_2);
					}

					if (lCount == 3)
					{
						GEO_PrimPoly *prim_poly_ptr = (GEO_PrimPoly *)gdp->appendPrimitive(GA_PRIMPOLY);
						GA_Offset prim_start_off = prim_poly_ptr->getVertexOffset(3);

						int v1 = currentMesh->GetPolygonVertex(i, 2);
						int v2 = currentMesh->GetPolygonVertex(i, 1);
						int v3 = currentMesh->GetPolygonVertex(i, 0);


						prim_poly_ptr->appendVertex(startptoff + v1);
						prim_poly_ptr->appendVertex(startptoff + v2);
						prim_poly_ptr->appendVertex(startptoff + v3);


						prim_poly_ptr->close();
						prim_group->add(prim_poly_ptr);
					}

				}
			}
			else
			{
				//std::cout << currentNode->GetName() << " has no mesh"<<std::endl;
				//std::cout << currentNode->GetName() << " has no polygon" << std::endl;
			}

			i_fbx(currentNode, aaa, gdp);


		}
	}



}


