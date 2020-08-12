#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){

    ofSetWindowTitle("Meme Explorer");
    
    // this should point to the json file containing your image files and tsne coordinates
    tsnePath = ofToDataPath("facebook_reddit_data5.json");
    
    //max number of images
    int numImgs = 200;

    // Max dimensions of images
    maxDim = 200;

    showText = false;
    showDate = false;
    showImage = false;

    // listen for scroll events, and save screenshot button press
    ofAddListener(ofEvents().mouseScrolled, this, &ofApp::mouseScrolled);
    save.addListener(this, &ofApp::saveScreenshot);
   // ofAddListener(ofEvents().keyPressed, this, &ofApp::keyPressed);
    
    gui.setup();
    gui.setName("Settings");
    gui.add(memes.set("Memes", true));
    gui.add(scale.set("Scale", 4.0, 0.0, 40.0));
    gui.add(imageSize.set("Image Size", 0.3, 0.0, 4.0));
    gui.add(showDate.set("Show Post Date", false));
    gui.add(showText.set("Show Source", false));
    gui.add(showSub.set("Show Subreddit", false));
    //gui.add(maxDim.set("Resolution", 50, 0, 300));

    gui.add(save.setup("Save Screenshot"));
    
    social.setup();
    social.setName("Social Media");
    social.add(reddit.set("Reddit", true));
    //social.add(twitter.set("Twitter", false));
    social.add(facebook.set("Facebook", false));
    social.setPosition(10, 175);

    ofJson js;
    ofFile file(tsnePath);
    parsingSuccessful = file.exists();
    
    if (!parsingSuccessful) {
        ofLog(OF_LOG_ERROR) << "parsing not successful";
        return;
    }
    
    thumbs.clear();
    
    // convert ofFile to ofJson obj
    file >> js;

    //changed ofVec2f to ofVec3f
    ofVec2f minPoint(1e8, 1e8);
    ofVec2f maxPoint(-1e8, -1e8);

    int imgCount = 0;

    for (auto & entry : js){

        /* Uncomment below to include a max number of images */
        //if(imgCount < numImgs){

            if(!entry.empty()) {

                string path = entry["path"];
                float x = entry["point"][0];
                float y = entry["point"][1];
                string social = entry["socialmedia"];
                string subreddit = entry["subreddit"];
                // string postDate = " ";
                // if (!entry["postDate"].is_null()){
                string postDate = entry["postDate"];
                //}
                // string timestamp = " ";
                /* TODO: Add an exception */
                // try {
                //     postDate = entry["postDate"];
                // }
                // catch (std::exception& e){
                //     cout << "no postDate data" << endl;
                // }
                    
                

                minPoint.x = min(minPoint.x, x);
                minPoint.y = min(minPoint.y, y);

                maxPoint.x = max(maxPoint.x, x);
                maxPoint.y = max(maxPoint.y, y);
                
                ImageThumb thumb;

                thumb.point.set(x, y);

                //TODO: Add a border box or background color for text!
                thumb.font.load("/Users/katyadonovan/Developer/openFrameworks/apps/myApps/ImageTSNEViewer/bin/data/Arial.ttf", 10);

                thumb.text = social;
                thumb.time = postDate;
                thumb.sub = subreddit;
                // thumb.time = timestamp;

                thumb.image.load(path);
                
                if (thumb.image.getWidth() > thumb.image.getHeight()) {
                    thumb.image.resize(maxDim, maxDim * thumb.image.getHeight() / thumb.image.getWidth());
                } else {
                    thumb.image.resize(maxDim * thumb.image.getWidth() / thumb.image.getHeight(), maxDim);
                }
                thumbs.push_back(thumb);
            }
            imgCount++;
        //} //imgNum end
    }

    for (int i=0; i<thumbs.size(); i++) {
        thumbs[i].point.set(ofMap(thumbs[i].point.x, minPoint.x, maxPoint.x, 0, 1),
                            ofMap(thumbs[i].point.y, minPoint.y, maxPoint.y, 0, 1));
    }

    position.set(-0.5 * ofGetWidth(), -0.5 * ofGetHeight());
}

//--------------------------------------------------------------
void ofApp::update(){
    
}

//--------------------------------------------------------------
void ofApp::draw(){
    ofBackgroundGradient(ofColor(0), ofColor(100));
    if (!parsingSuccessful) {
        ofDrawBitmapString("Could not find file "+tsnePath+"\nSee the instructions for how to create one.", 50, 50);
        return;
    }
    
    ofPushMatrix();
    ofTranslate(position.x * (scale - 1.0), position.y * (scale - 1.0));

    for (int i=0; i<thumbs.size(); i++) {
        float x = ofMap(thumbs[i].point.x, 0, 1, 0, scale * ofGetWidth());
        float y = ofMap(thumbs[i].point.y, 0, 1, 0, scale * ofGetHeight());

        string social = thumbs[i].text;
        string time = thumbs[i].time;
        string sub = thumbs[i].sub;

        if(reddit && thumbs[i].text=="reddit"){
            thumbs[i].image.draw(x, y, imageSize * thumbs[i].image.getWidth(), imageSize * thumbs[i].image.getHeight());
            if(showText){
                thumbs[i].font.drawString(social, x, y);
                showDate = false;
                showSub = false;
            }
            else if(showDate){
                thumbs[i].font.drawString(time, x, y);
                showText = false;
                showSub = false;
            }
            else if (showSub){
                thumbs[i].font.drawString(sub, x, y);
                showText = false;
                showDate = false;
            }

        }

        if(facebook && thumbs[i].text=="facebook"){
            thumbs[i].image.draw(x, y, imageSize * thumbs[i].image.getWidth(), imageSize * thumbs[i].image.getHeight());
            if(showText){
                thumbs[i].font.drawString(social, x, y);
                showDate = false;
                showSub = false;
            }
            else if(showDate){
                thumbs[i].font.drawString(time, x, y);
                showText = false;
                showSub = false;
            }
            else if(showSub){
                thumbs[i].font.drawString(sub, x, y);
                showText = false;
                showDate = false;
            }
        }

        // if(showDate){
        //     showText.set(false);
        // }

        // if(showText){
        //     showDate.set(false);
        // }

    }

    ofPopMatrix();
    gui.draw();
    social.draw();
}

//--------------------------------------------------------------
void ofApp::saveScreenshot(){
    ofFbo fbo;
    fbo.allocate(scale * ofGetWidth() + 100, scale * ofGetHeight() + 100);
    fbo.begin();
    ofClear(0, 0);
    ofBackground(0);
    for (int i=0; i<thumbs.size(); i++) {
        float x = ofMap(thumbs[i].point.x, 0, 1, 0, scale * ofGetWidth());
        float y = ofMap(thumbs[i].point.y, 0, 1, 0, scale * ofGetHeight());
        thumbs[i].image.draw(x, y, imageSize * thumbs[i].image.getWidth(), imageSize * thumbs[i].image.getHeight());
    }
    fbo.end();
    ofPixels pix;
    ofImage img;
    fbo.readToPixels(pix);
    img.setFromPixels(pix);
    img.save("out.png");
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){

    switch(key){
        case 'f':
            showText = !showText;
        break;
        case 't':
          //  showDate = !showDate;
        break;
        case 'x':
            showImage = !showImage;
        break;
    }
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){
    position.x = position.x - (ofGetMouseX()-ofGetPreviousMouseX());
    position.y = position.y - (ofGetMouseY()-ofGetPreviousMouseY());
}

//--------------------------------------------------------------
void ofApp::mouseScrolled(ofMouseEventArgs &evt) {
    scale.set(ofClamp(scale + 0.5 * (evt.scrollY), 0.0, 40.0));
}


//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}