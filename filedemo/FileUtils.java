package com.system;

import java.io.File;
import java.io.IOException;

/**
 * Created by Administrator on 2018/6/27.
 */

public class FileUtils {
    public final static String rootPath = "E:" + File.separator + "xp" + File.separator;
    public final static String rootPathDirA = rootPath + "a";
    public final static String rootPathDirB = rootPath + "b";
    public final static String rootPathDirC = rootPath + "c";
    public final static String rootPathFileA1 = rootPathDirA + File.separator + "a1.txt";
    public final static String rootPathFileA2 = rootPathDirA + File.separator + "a2.txt";
    public final static String rootPathFileAA2 = rootPathDirA + File.separator + "aa2.txt";
    public final static String rootPathFileB1 = rootPathDirB + File.separator + "b.txt";

    public static void main(String args[]) throws IOException {
        File file = new File(rootPath);
        if (isExists(file)) {
            //对目录A进行操作
            opeateA(rootPathDirA, rootPathFileA1, rootPathFileA2, rootPathFileAA2);
            //对目录B进行操作
            opeateB(rootPathDirB, rootPathFileB1);
            //创建C文件
            creatDir(rootPathDirC);
        }
    }


    /**
     * 对A目录下的文件进行操作
     *
     * @param filePathA   A目录的根路径
     * @param filePathA1  A1要删除的的文件路径
     * @param filePathA2  A2修改前名字的路径
     * @param filePathAA2 AA2修改后名字的路径
     */
    private static void opeateA(String filePathA, String filePathA1, String filePathA2, String filePathAA2) {
        File file = new File(filePathA);
        if (isExists(file)) {
            deleteFile(filePathA1);
            reNameFile(filePathA2, filePathAA2);
        }
    }

    /**
     * 对B目录下的文件进行操作
     *
     * @param filePathB  B目录的根路径
     * @param filePathB1 B1要删除的的文件路径
     * @throws IOException 操作时可能会出现IO流的异常
     */
    private static void opeateB(String filePathB, String filePathB1) throws IOException {
        File file = new File(filePathB);
        if (isExists(file)) {
            createFile(filePathB1);
        }
    }

    /**
     * 重命名文件
     *
     * @param filePath1 原命名路径的文件
     * @param filePath2
     */
    private static void reNameFile(String filePath1, String filePath2) {
        File file1 = new File(filePath1);
        File file2 = new File(filePath2);
        if (isExists(file1)) {
            file1.renameTo(file2);
        }
    }

    /**
     * 删除文件
     *
     * @param filePath 文件路径
     */
    private static void deleteFile(String filePath) {
        File file = new File(filePath);
        if (isExists(file)) {
            file.delete();
        }
    }

    /**
     * 创建文件夹
     *
     * @param filePath 文件路径
     */
    private static void creatDir(String filePath) {
        File file = new File(filePath);
        if (!isExists(file)) {
            file.mkdir();
        }
    }

    /**
     * 创建文件
     *
     * @param filePath 文件路径
     * @throws IOException
     */
    private static void createFile(String filePath) throws IOException {
        File file = new File(filePath);
        if (!isExists(file)) {
            file.createNewFile();
        }
    }

    /**
     * file对象是否存在
     *
     * @param file 文件对象
     * @return
     */
    private static boolean isExists(File file) {
        boolean exists = file.exists();
        String str = exists ? "目录存在:" : "目录不存在:";
        String filePath = file.getAbsolutePath();
        System.out.println(str + filePath);
        return exists;
    }

}
