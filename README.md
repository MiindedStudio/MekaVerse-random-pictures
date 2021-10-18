# MekaVerse-random
Script for the creation of metadata and the randomization of images of MekaVerse

## Step to replay the random : 
1. Create a folder : ``output``
2. Retrieve the 8,888 images (48gb) without renaming them, and put them in the ``output`` folder.
3. Delete from ``output`` folder the image of Meka #5227 that was added after : ``camogreen_darkgrey_lightgreen_camogreen_lightgreen_lightgreen_C_4C_4C_6C_1C_3C_2C_0_0_0_0_0_0_2033.png``.
4. Add in the ``output`` folder the placeholder by naming it ``1080_placeholder.png``
5. Add in the ``output`` folder a file named ``Thumbs.db`` that had nothing to do with it.
6. The random was launched before the revelation of Legendary Mekas, so you must remove legendary pictures and put 4 files in ``output`` folder : 
``Legendary_Meka_Tickets_1.png``, ``Legendary_Meka_Tickets_2.png``, ``Legendary_Meka_Tickets_3.png``, ``Legendary_Meka_Tickets_4.png``
7. Run the python script ``python set_metadata.py``

The ``generation.json`` file show you exactly the same result as on OpenSea (with missing metadata for the Meka #5227)
