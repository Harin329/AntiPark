//
//  VisionManager.swift
//  AntiPark
//
//  Created by Harin Wu on 2024-10-27.
//

import Foundation
import SwiftUI
import Vision

class VisionManager {
    private var request: VNDetectHumanRectanglesRequest
    
    private var isProcessing: Bool = false
    private var addToObservationStream: (([VNHumanObservation]) -> Void)?
    
    lazy var observationStream: AsyncStream<[VNHumanObservation]> = {
        AsyncStream { continuation in
            addToObservationStream = { observations in
                continuation.yield(observations)
            }
        }
    }()
    
    init() {
        var request = VNDetectHumanRectanglesRequest()
        request.upperBodyOnly = true
        self.request = request
    }
    
    func processHumanDetection(_ ciImage: CIImage) {
        print("processing: \(isProcessing)")
        
        if (isProcessing) {
            return
        }
        isProcessing = true
        defer {
            isProcessing = false
        }
        print("processing")
        let handler = VNImageRequestHandler(ciImage: ciImage)
        
        Task {
            try handler.perform([self.request])
            
            guard let results = request.results else {
                print("No results found")
                return
            }
            print(results)
        }
    }
}
