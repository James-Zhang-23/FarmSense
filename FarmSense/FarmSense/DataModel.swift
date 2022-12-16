//
//  DataModel.swift
//  FarmSense
//
//  Created by Yuzhe Zhang on 12/12/22.
//

import Foundation
import SwiftUI

 struct Data: Decodable {
     var air_humidity: Double
     var air_pressure: Double
     var air_temperature: Double
     var soil_humidity: Double
     var soil_temperature: Double
 }

struct Suggestion: Decodable {
    var roof: Int
    var water: Int
}

