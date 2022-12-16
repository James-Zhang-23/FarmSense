//
//  ContentView.swift
//  FarmSense
//
//  Created by Yuzhe Zhang on 12/12/22.
//

import SwiftUI

struct ContentView: View {
    
    @State var data =  Data(air_humidity: 39.0, air_pressure: 100.0, air_temperature: 22.0, soil_humidity: 38.0, soil_temperature: 20.0)
    
    @State var suggestion = Suggestion(roof: 0, water: 1)
    @State var GraphicStatus = "🪴"
    @State var WaterStatus = "WATER WORKS FINE"
    @State var RoofStatus = "ROOF WORKS FINE"
    
    @State var RoofLight = Color.green
    @State var WaterLight = Color.green
    
    @State var SoilTempLight = Color.green
    @State var SoilMoistureLight = Color.green
    @State var AirTempLight = Color.green
    @State var AirMoistureLight = Color.green
    
    func getData() {
        let url = URL(string: "http://34.219.234.246:5000/getdata")
        print("getting data")
        URLSession.shared.dataTask(with: url!) {data, _, error in
            DispatchQueue.main.async {
                print("connecting")
                if let data = data {
                    do{
                        print("connected")
                        let decoder = JSONDecoder()
                        print("decoding")
                        let decodedData = try decoder.decode(Data.self, from: data)
                        print("decoded")
                        self.data = decodedData
                        print("success")
                        print(data)
                    } catch {
                        print("Error")
                    }
                }
            }
        }.resume()
    }
    
    func getSuggestion() {
        let url = URL(string: "http://34.219.234.246:5000/suggestion")
        print("getting suggestion")
        URLSession.shared.dataTask(with: url!) {suggestion, _, error in
            DispatchQueue.main.async {
                print("connecting")
                if let suggestion = suggestion {
                    do{
                        print("connected")
                        let decoder = JSONDecoder()
                        print("decoding")
                        let decodedData = try decoder.decode(Suggestion.self, from: suggestion)
                        print("decoded")
                        self.suggestion = decodedData
                        print("success")
                        print(suggestion)
                    } catch {
                        print("Error")
                    }
                }
            }
        }.resume()
    }
    
    var body: some View {
                
                VStack {
                    HStack{
                        Text("FarmSense").font(Font.custom("FONTSPRING DEMO - Blue Vinyl", size:35))
                        Spacer()
                        Button(action:{
                            self.getData()
                            if data.air_temperature > 35{
                                AirTempLight = Color.yellow
                            }
                            if data.air_temperature > 40{
                                AirTempLight = Color.red
                            }
                            if data.air_humidity > 50 || data.air_humidity < 35{
                                AirMoistureLight = Color.yellow
                            }
                            if data.air_humidity > 70 || data.air_humidity < 30{
                                AirMoistureLight = Color.red
                            }
                            if data.soil_temperature > 30{
                                SoilTempLight = Color.yellow
                            }
                            if data.soil_temperature > 35{
                                SoilTempLight = Color.red
                            }
                            if data.soil_humidity > 45 || data.soil_humidity < 30{
                                SoilMoistureLight = Color.yellow
                            }
                            if data.soil_humidity > 60 || data.soil_humidity < 20{
                                SoilMoistureLight = Color.red
                            }
                            if data.soil_humidity < 45 && data.soil_humidity > 30{
                                SoilMoistureLight = Color.green
                            }
                            self.getSuggestion()
                            if suggestion.roof == 1{
                                RoofStatus = "PLEASE OPEN ROOF"
                                RoofLight = Color.red
                            }
                            if suggestion.water == 0{
                                WaterStatus = "PLEASE CLOSE WATER"
                                WaterLight = Color.yellow
                                GraphicStatus = "💦"
                            }
                            if suggestion.water == 2{
                                WaterStatus = "PLEASE OPEN WATER"
                                WaterLight = Color.red
                                GraphicStatus = "🏜️"
                            }
                        }){
                            Image(systemName: "arrow.clockwise").foregroundColor(.orange).bold()
                        }
                    }.padding(.top, 15).padding(.bottom,1).padding(.horizontal,20)
                    
                    HStack{
                            Text("           ")
                            Text(GraphicStatus).font(.system(size:55))
                            Text("         ")
                            VStack(alignment: .leading){
                                HStack{
                                    Text(WaterStatus).font(.system(size:15).bold())
                                    Spacer()
                                    RoundedRectangle(cornerRadius: 2, style: .continuous)
                                        .fill(WaterLight)
                                        .frame(width: 55, height: 5)
                                }
                                HStack{
                                    Text(RoofStatus).font(.system(size:15).bold())
                                    Spacer()
                                    RoundedRectangle(cornerRadius: 2, style: .continuous)
                                        .fill(RoofLight)
                                        .frame(width: 55, height: 5)
                                }
                                
                            }
                    }.padding(.top,5).padding(.trailing,35)
                    
                    ZStack{
                            
                            Color.white.opacity(0.7).blur(radius: 200)
                            
                            Circle()
                                .fill(Color.yellow)
                                .padding(100)
                                .blur(radius: 120)
                                .offset(x: 200, y: -200)
                            
                            Circle()
                                .fill(Color.orange)
                                .padding(80)
                                .blur(radius: 120)
                                .offset(x: -200, y: -100)
                            
                            Circle()
                                .fill(Color.yellow)
                                .padding(100)
                                .blur(radius: 120)
                                .offset(x: 100, y: 100)
                        
                        RoundedRectangle(cornerRadius: 18, style: .continuous)
                            .fill(Color.gray.opacity(0.1))
                            .frame(width: 410, height: 750)
                        
                        VStack{
                            Spacer().frame(minHeight: 30 ,idealHeight: 30,maxHeight: 30)
                                .fixedSize()
                            HStack{
                                
                                ZStack{
                                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                                        .fill(.white)
                                        .opacity(0.1)
                                        .background(
                                            Color.white
                                                .opacity(0.08)
                                                .blur(radius: 10)
                                        )
                                        .background(
                                            RoundedRectangle(cornerRadius: 18, style: .continuous)
                                                .stroke(
                                                    .linearGradient(.init(colors:[
                                                        .yellow.opacity(0.5),
                                                        .yellow.opacity(0.2),
                                                        .clear,
                                                        .clear,
                                                        .orange.opacity(0.5),]), startPoint: .topLeading, endPoint: .bottomTrailing),lineWidth: 1.5)
                                        )
                                        .frame(width: 170, height: 170)
                                        .shadow(color: .black.opacity(0.1),radius: 5,x:-5,y:-5)
                                    VStack{
                                        HStack{
                                            Text("Soil Moisture").font(.system(size:18).bold())
                                            Circle().fill(SoilMoistureLight).frame(width:10,height:10)
                                        }
                                        Text("")
                                        HStack{
                                            Text("\(Int(data.soil_humidity))").font(.system(size:60).italic().bold())
                                            Text("RH").padding(.top,30)
                                        }
                                    }.padding()
                                    
                                }
                                Spacer().frame(minWidth: 30,idealWidth: 30,maxWidth: 30)
                                    .fixedSize()
                                ZStack{
                                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                                        .fill(.white)
                                        .opacity(0.1)
                                        .background(
                                            Color.white
                                                .opacity(0.08)
                                                .blur(radius: 10)
                                        )
                                        .background(
                                            RoundedRectangle(cornerRadius: 18, style: .continuous)
                                                .stroke(
                                                    .linearGradient(.init(colors:[
                                                        .yellow.opacity(0.5),
                                                        .yellow.opacity(0.2),
                                                        .clear,
                                                        .clear,
                                                        .orange.opacity(0.5),]), startPoint: .topLeading, endPoint: .bottomTrailing),lineWidth: 1.5)
                                        )
                                        .frame(width: 170, height: 170)
                                        .shadow(color: .black.opacity(0.1),radius: 5,x:-5,y:-5)
                                    VStack{
                                        HStack{
                                            Text("Soil Temp").font(.system(size:18).bold())
                                            Circle().fill(SoilTempLight).frame(width:10,height:10)
                                        }
                                        Text("")
                                        HStack{
                                            Text("\(Int(data.soil_temperature))").font(.system(size:60).italic().bold())
                                            Text("˚C").padding(.top,30)
                                        }
                                    }.padding()
                                    
                                }
                            }.padding(.top,5)
                            HStack{
                                ZStack{
                                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                                        .fill(.white)
                                        .opacity(0.1)
                                        .background(
                                            Color.white
                                                .opacity(0.08)
                                                .blur(radius: 10)
                                        )
                                        .background(
                                            RoundedRectangle(cornerRadius: 18, style: .continuous)
                                                .stroke(
                                                    .linearGradient(.init(colors:[
                                                        .yellow.opacity(0.5),
                                                        .yellow.opacity(0.2),
                                                        .clear,
                                                        .clear,
                                                        .orange.opacity(0.5),]), startPoint: .topLeading, endPoint: .bottomTrailing),lineWidth: 1.5)
                                        )
                                        .frame(width: 170, height: 170)
                                        .shadow(color: .black.opacity(0.1),radius: 5,x:-5,y:-5)
                                    VStack{
                                        HStack{
                                            Text("Air Moisture").font(.system(size:18).bold())
                                            Circle().fill(AirMoistureLight).frame(width:10,height:10)
                                        }
                                        Text("")
                                        HStack{
                                            Text("\(Int(data.air_humidity))").font(.system(size:60).italic().bold())
                                            Text("RH").padding(.top,30)
                                        }
                                    }.padding()
                                    
                                }
                                Spacer().frame(minWidth: 30,idealWidth: 30,maxWidth: 30)
                                    .fixedSize()
                                ZStack{
                                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                                        .fill(.white)
                                        .opacity(0.1)
                                        .background(
                                            Color.white
                                                .opacity(0.08)
                                                .blur(radius: 10)
                                        )
                                        .background(
                                            RoundedRectangle(cornerRadius: 18, style: .continuous)
                                                .stroke(
                                                    .linearGradient(.init(colors:[
                                                        .yellow.opacity(0.5),
                                                        .yellow.opacity(0.2),
                                                        .clear,
                                                        .clear,
                                                        .orange.opacity(0.5),]), startPoint: .topLeading, endPoint: .bottomTrailing),lineWidth: 1.5)
                                        )
                                        .frame(width: 170, height: 170)
                                        .shadow(color: .black.opacity(0.1),radius: 5,x:-5,y:-5)
                                    VStack{
                                        HStack{
                                            Text("Air Temp").font(.system(size:18).bold())
                                            Circle().fill(AirTempLight).frame(width:10,height:10)
                                        }
                                        Text("")
                                        HStack{
                                            Text("\(Int(data.air_temperature))").font(.system(size:60).italic().bold())
                                            Text("˚C").padding(.top,30)
                                        }
                                    }.padding()
                                   
                                }
                            }.padding(.top,20)
                            
                            HStack{
                                ZStack{
                                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                                        .fill(.white)
                                        .opacity(0.1)
                                        .background(
                                            Color.white
                                                .opacity(0.08)
                                                .blur(radius: 10)
                                        )
                                        .background(
                                            RoundedRectangle(cornerRadius: 18, style: .continuous)
                                                .stroke(
                                                    .linearGradient(.init(colors:[
                                                        .yellow.opacity(0.5),
                                                        .yellow.opacity(0.2),
                                                        .clear,
                                                        .clear,
                                                        .orange.opacity(0.5),]), startPoint: .topLeading, endPoint: .bottomTrailing),lineWidth: 1.5)
                                        )
                                        .frame(width: 370, height: 80)
                                        .shadow(color: .black.opacity(0.1),radius: 5,x:-5,y:-5)
                                    HStack{
                                        Text("Air Pressure").font(.system(size:18).bold())
                                        Text("")
                                        Text("\(Int(data.air_pressure))").font(.system(size:28).italic().bold())
                                        Text("kPa")
                                    }.padding()
                                    
                                }
                            }.padding(.top,25)
                            HStack{
                                ZStack{
                                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                                        .fill(LinearGradient(gradient: Gradient(colors:[Color("Light Blue"), Color("Blue")]),startPoint: .top,endPoint: .bottom))
                                        .frame(width: 150, height: 50)
                                    Image(systemName: "drop").bold().foregroundColor(Color.white)
                                }
                                Text("      ")
                                ZStack{
                                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                                        .fill(LinearGradient(gradient: Gradient(colors:[Color("Light Blue"), Color("Blue")]),startPoint: .top,endPoint: .bottom))
                                        .frame(width: 150, height: 50)
                                    Image(systemName: "house").bold().foregroundColor(Color.white)
                                }
                                
                            }.padding(.top,25)
                            
                            Text("Designed by Nova in USC").font(.system(size:10).bold()).padding(.top,20)
                            Spacer()
                            
                        }
                    
                        
                        
                        
                        
                        
                    }.padding(.top,1).ignoresSafeArea()
                }.padding(.top,75)
            
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

extension HorizontalAlignment {
    private enum HAlignment: AlignmentID {
        static func defaultValue(in dimensions: ViewDimensions) -> CGFloat {
            return dimensions[HorizontalAlignment.leading]
        }
    }
    static let myHAlignment = HorizontalAlignment(HAlignment.self)
}
