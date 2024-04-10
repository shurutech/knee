
# Install VMware Fusion on Apple chip-based Mac machine
1. Go to the [VMware Customer Connect registration page](https://customerconnect.vmware.com/account-registration) and fill in the required details with utmost accuracy. It is also important to confirm your email address to ensure the proper activation of your profile.
2. Go to the [VMware Fusion downloads page](https://customerconnect.vmware.com/downloads/details?downloadGroup=FUS-1302&productId=1375&rPId=105193) and choose the 13.0.2 version to download the VMware Fusion. If prompted, login to your VMware Customer Connect profile. If you do not have a profile, please create one.
3. Open the Finder app and navigate to the Downloads directory in your Mac machine.
4. Open the VMware Fusion package, then double-click the icon and follow the onscreen instructions.
5. During the installation process, a license key prompt appears. Within the same window, you'll find a Get a Free License Key button. Simply click this button to obtain the personal use license key and complete the installation.



# Install Vagrant and its plugins on Apple chip-based Mac machine
Step 1: Tap HashiCorp Repository
```
 brew tap hashicorp/tap
```
Step 2: Install Vagrant 
```
brew install hashicorp/tap/hashicorp-vagrant
```
Step 3: Verify Installation
```
vagrant --version
```

# Install Vagrant VMware utility
1. Download the [Vagrant VMware utility package](https://releases.hashicorp.com/vagrant-vmware-utility/1.0.22/vagrant-vmware-utility_1.0.22_darwin_amd64.dmgs).
2. Open the Finder app and navigate to the Downloads directory in your Mac machine.
3. Open the Vagrant VMware utility package, then double-click the icon and follow the onscreen instructions.
Install

# Install Vagrant VMware provider plugin
```
vagrant plugin install vagrant-vmware-desktop
```
**Note**: vagrant template(Vagrantfile) already exists in the repo. You can customize it as per your requirement.















