import numpy as np


def subobject_map_from_mergelist(mergelist_content):
    """
    Extracts a single object layer from a mergelist and returns a map of subobject ID > object ID.
    If one subobject is contained in more than one object, the last object is kept.
    :param mergelist_content:
        the mergelist content as a string
    """
    subobjects_map = {}
    for line in mergelist_content.split("\n")[0::4]:
        elems = line.split()
        if len(elems) > 0:
            object_id = elems[0]
            for subobject_id in elems[3:]:
                subobjects_map[np.uint64(subobject_id)] = np.uint64(object_id)
    return subobjects_map


def apply_mergelist(segmentation, mergelist_content, background_id=0, pad=0):
    """
    Merges subobjects using a dictionary of (subobject, object) pairs. So each subobject can only be member of one object.
    The resulting segmentation for each merged group contains only the first ID of that group
    :param segmentation:
        3D array containing the subobject IDs
    :param mergelist_content:
        the mergelist content as a string
    :param pad:
        optional padding that is excluded from mergelist application
    """
    raise "this is slow and broken, don't use the fallback. compile the cython sources using setup.py install"


def gen_mergelist_from_segmentation(segmentation, background_id=0, pad=0, offsets=np.array([0, 0, 0], dtype=np.uint64)):
    """
    Generates a mergelist from a segmentation in which each subobject is contained in its own object.
    The object's coordinate is the first coordinate of the subobject.
    :param segmentation:
        3D array containing the subobject IDs
    :background_id:
        The background id will be skipped
    :pad:
        optional padding that is excluded from mergelist generation
    :offsets:
        the voxel coordinate closest to 0, 0, 0 of the whole dataset, used to give objects their correct coordinate
    """
    width = segmentation.shape[0]
    height = segmentation.shape[1]
    depth = segmentation.shape[2]
    so_cache = background_id

    seen_subobjects = set()
    new_mergelist = ""
    for z in xrange(pad, depth - pad):
        for y in xrange(pad, height - pad):
            for x in xrange(pad, width - pad):
                next_id = segmentation[x, y, z]
                if next_id == so_cache or next_id == background_id or next_id in seen_subobjects:
                    continue
                so_cache = next_id
                seen_subobjects.add(next_id)
                new_mergelist += "{0} 0 0 {0}\n{1} {2} {3}\n\n\n".format(next_id, int(offsets[0]+x), int(offsets[1]+y), int(offsets[2]+z))
    return new_mergelist
