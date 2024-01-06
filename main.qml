import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls 2.0
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Extras.Private 1.0


ApplicationWindow{
    id : root
    width: 400
    height: 400
    title:"Smart Parking"
    visible: true  
    flags: Qt.Window
	color:"white"
	
	signal updateParkingSlots(int index, bool isEmpty)
	

    Text{
        id : text1
        anchors.horizontalCenter: parent.horizontalCenter
        y:80
        text:"SMART PARKING MANAGEMENT SYSTEM"
        color: "steelblue"
        font.family  : "Times New Roman"
        font.pixelSize: 35
        font.bold : true
    }
	Text{
		anchors.horizontalCenter: parent.horizontalCenter
		y:125
		text : "Oleh: Kelompok 2"
		color : "steelblue"
		font.pixelSize : 30
		font.family:"Times New Roman"
	}
	Image{
		x:20
		y:10
		width : 150
		height : 180
		source:"upilogo.png"				
	}
	Image{
		x:1750
		y:10
		width : 150
		height : 200
		source : "parkir.png"
	
	}
    
    ListModel {
        id: parkingSlots
        ListElement { filled: true }
        ListElement { filled: true }
        ListElement { filled: false }
        ListElement { filled: false }
        
    }
    
    Repeater {
        model: parkingSlots
        Rectangle {
            property bool filled: model.filled
        
            x: 500 + index * (width + 60)
            y: 200
            width: 200
            height: 250
			radius:20
            color: filled ? "red" : "lightgreen"
            
            Image {
            source: filled ? "car.png" : ""
            width : 190
            height : 190
            anchors.centerIn: parent
            visible: filled
           }
            
           Text {
            text: "A" + (index + 1)
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 20
        }

        Text {
            text: filled ? "" : "Available"
			anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            font.pixelSize: 20
            font.bold : true
           }
           
        // Connect the signal to the appropriate function
            Connections {
            target: ParkingController  // Replace with the actual object name of ParkingController
            onUpdateParkingSlots: {
            // Handle the signal here
            console.log("Slot at index", index, "is", isEmpty ? "empty" : "filled");

            // Update the model directly
            parkingSlots.setProperty(index, "filled", !isEmpty);

            // Update the "Available Slots" text
            var filledCount = 0;
            for (var i = 0; i < parkingSlots.count; ++i) {
            if (parkingSlots.get(i).filled)
                filledCount++;
            }
            availableSlots.text = "Available Slots: " + (4 - filledCount);

            // Add any other actions or UI updates you need
        }
    }

        }
    }
	Rectangle {
		width: 300
		height: 50
		x:800
		y:550
		color: "lightblue"
		border.color: "blue"
		radius: 10

		Text {
			id: availableSlots
			anchors.centerIn: parent
			text: "Available Slots: " + (4 - parkingSlots.get(0).filled - parkingSlots.get(1).filled)
			font.pixelSize: 25
			font.bold: true
			color: "steelblue"
		}
	}



   
}