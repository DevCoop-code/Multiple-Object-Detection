package com.hankyo.jeong.rtobjectdetectorsample.fragment;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.util.SparseIntArray;
import android.view.LayoutInflater;
import android.view.Surface;
import android.view.View;
import android.view.ViewGroup;

import com.hankyo.jeong.rtobjectdetectorsample.R;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link CameraConnectionFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class CameraConnectionFragment extends Fragment {

    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    // Camera Preview size will be chosen to be the smallest frame by pixel size capable of containing a DESIRED_SIZE x DESIRED_SIZE square
    private static final int MINIMUM_PREVIEW_SIZE = 320;

    // Conversion from screen rotation to JPEG orientation
    private static final SparseIntArray ORIENTATIONS = new SparseIntArray();
    private static final String FRAGMENT_DIALOG = "dialog";

    static {
        ORIENTATIONS.append(Surface.ROTATION_0, 90);
        ORIENTATIONS.append(Surface.ROTATION_90, 0);
    }

    public CameraConnectionFragment() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment CameraConnectionFragment.
     */
    // TODO: Rename and change types and number of parameters
    public static CameraConnectionFragment newInstance(String param1, String param2) {
        CameraConnectionFragment fragment = new CameraConnectionFragment();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_camera_connection, container, false);
    }
}