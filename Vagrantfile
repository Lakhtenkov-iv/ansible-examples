# -*- mode: ruby -*-
# vi: set ft=ruby :

i = 2

Vagrant.configure("2") do |config|

  (1..i).each do |i|
    config.vm.box = "sbeliakou/centos-7.3-x86_64-minimal"
    config.vm.network "forwarded_port", guest: 8080, host: "808#{i-1}"

    config.vm.hostname = "pet-#{i}"
  
    config.vm.provider "virtualbox" do |vb|
      vb = config.vm.hostname
    end
  end
end
