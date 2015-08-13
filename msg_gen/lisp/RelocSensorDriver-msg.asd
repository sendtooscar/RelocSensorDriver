
(cl:in-package :asdf)

(defsystem "RelocSensorDriver-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Relocdata" :depends-on ("_package_Relocdata"))
    (:file "_package_Relocdata" :depends-on ("_package"))
  ))