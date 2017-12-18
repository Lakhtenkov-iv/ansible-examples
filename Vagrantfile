# -*- mode: ruby -*-
# vi: set ft=ruby :

vm_count = 1

Vagrant.configure("2") do |config|

  (1..vm_count).each do |vm_count|
    config.vm.box = "sbeliakou/centos-7.3-x86_64-minimal"
    config.vm.network "forwarded_port", guest: 8080, host: "808#{vm_count-1}"

    config.vm.hostname = "pet-#{vm_count}"
  
    config.vm.provider "virtualbox" do |vb|
      vb = config.vm.hostname
    end
  end
end
