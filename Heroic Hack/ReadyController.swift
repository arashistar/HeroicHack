//
//  ReadyController.swift
//  Heroic Hack
//
//  Created by Courtney Storm on 10/20/18.
//  Copyright © 2018 Courtney Storm. All rights reserved.
//

import UIKit

class ReadyController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {


    @IBOutlet weak var imageView: UIImageView!
    
    
    let imagePickerController = UIImagePickerController()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    

    @IBAction func chooseImage(_ sender: Any) {
        
        imagePickerController.delegate = self
        
        let actionSheet = UIAlertController(title: "Photo Source", message: "How do you want mosy?", preferredStyle: .actionSheet)
        
        actionSheet.addAction(UIAlertAction(title: "Use Camera", style: .default, handler: { (action:UIAlertAction) in
            if UIImagePickerController.isSourceTypeAvailable(.camera) {
                self.imagePickerController.sourceType = .camera
                self.present(self.imagePickerController, animated: true, completion: nil)
            }else{
                print("Camera not available :(")
            }
            
        }))
        
        actionSheet.addAction(UIAlertAction(title: "Select from Photo Library", style: .default, handler: { (action:UIAlertAction) in
            self.imagePickerController.sourceType = .photoLibrary
            self.present(self.imagePickerController, animated: true, completion: nil)
        }))
        
        actionSheet.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: nil ))
        
        self.present(actionSheet, animated: true, completion: nil)
        
    }

    @objc(imagePickerController:didFinishPickingMediaWithInfo:) func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        self.imageView.image = info[UIImagePickerController.InfoKey.originalImage] as? UIImage
//        let image = info[UIImagePickerController.InfoKey.originalImage] as? UIImage
//        imageView.image = image
        
        picker.dismiss(animated: true, completion: nil)
        
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true, completion: nil)
    }

}
