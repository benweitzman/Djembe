DJEMBE
A django based torrent tracker and frontend extended by plugins for different applications.



Tracker:
Operates identically to conventional trackers, just implemented in python. View
 http://en.wikipedia.org/wiki/BitTorrent_tracker for more information. Based on
 protocal defined: http://wiki.theory.org/BitTorrentSpecification



The tracker uses a database of peers to log which users are downloading which
 torrents and the progress attributed to said torrents.
Each torrent is dynamically generated with an announce URL which includes the
 users private key.



Plugins:
Each plugin defines one model that has a one-to-one relationship with a torrent.
 These act as the 'atomic' unit of each plugin. These atomic units are grouped
 together in increasingly complex ways to organize torrents in whatever way
 makes sense for the given plugin.


 Music

  The top level model in Music is Artist. Each artist (or group of artist)
   has a number of Albums, and each Album can have a number of Album Release
   each having a number of Release Formats, the atomic unit for this plugin.
   The general flow and UI is based off of what.cd


 Movies

  This plugin operates similarly to above: People > Movie > Edition > Movie Format
   (The relationship between Movie and People is split into four categories: Actors,
   Producers, Writers, and Directors where Actors have an additional property relating
   them to the movie, which is the Role).

 Backup

  The top level is the Backup User > Backup > Version. The Backup User requires a
   special kind of UserProfile because of a number of special cases regarding ratio.
  The Backup plugin is intended to create a platform for users to trade unused
   harddrive space for offsite backup and redundancy. The rules governing the ratio
   are as follows:

    -Users have to backup other users content as much as they want their content
     backed up. For example, if a User wants to back up a 1GB file with 5x redundancy
     they will need to download a total of 5GB of other users content.

    -A priority system is associated with torrents that have not yet reached their
     desired redundancy.

    -Each User of the site has a number of priority points that they can use to
     incentivize users to backup their content. Priority points are assigned to
     backups as a whole. Each version inherits the priority points of its parent.