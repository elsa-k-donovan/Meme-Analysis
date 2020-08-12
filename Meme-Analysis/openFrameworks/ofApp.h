#pragma once

#include "ofMain.h"
#include "ofxGui.h"


struct ImageThumb {
public:
    ofImage image;
    ofPoint point;
	ofTrueTypeFont font;
	string text;
	string time;
	string sub;
    float t;
};

class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();
    
        void saveScreenshot();
    
		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
        void mouseScrolled(ofMouseEventArgs &evt);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void mouseEntered(int x, int y);
		void mouseExited(int x, int y);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
		
    vector<ImageThumb> thumbs;

    float maxDim;

	// changed to ofVec3f
    ofVec2f position;

	ofParameter<bool> memes;
    ofParameter<float> scale;
    ofParameter<float> imageSize;
	// ofParameter<int> maxDim;
	ofParameter<bool> reddit;
	ofParameter<bool> twitter;
	ofParameter<bool> facebook;
	ofParameter<bool> showDate;
	ofParameter<bool> showSub;
	ofParameter<bool> showText;
    ofxButton save;
    ofxPanel gui;
	ofxPanel social;
    
    string tsnePath;
    bool parsingSuccessful;
	ofRectangle rect;
	//bool showText;
	//bool showDate;
	bool showImage;
};