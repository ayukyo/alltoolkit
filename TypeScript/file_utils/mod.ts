/**
 * File Utilities - TypeScript File Operations Module
 *
 * A zero-dependency file utility module for TypeScript/Node.js.
 * Provides common file operations with proper error handling.
 *
 * @module file_utils
 * @version 1.0.0
 * @author AllToolkit
 */

import * as fs from 'fs';
import * as path from 'path';
import { createHash } from 'crypto';

export interface ReadFileOptions {
  encoding?: BufferEncoding | null;
  default?: string | Buffer;
}

export interface WriteFileOptions {
  encoding?: BufferEncoding;
  createDirs?: boolean;
  atomic?: boolean;
  mode?: number;
}

export interface ListFilesOptions {
  recursive?: boolean;
  includeDirs?: boolean;
  pattern?: string;
  sortBy?: 'name' | 'size' | 'mtime' | 'ctime';
  order?: 'asc' | 'desc';
}

export interface FileInfo {
  path: string;
  name: string;
  size: number;
  sizeHuman: string;
  isDirectory: boolean;
  isFile: boolean;
  isSymbolicLink: boolean;
  created: Date;
  modified: Date;
  accessed: Date;
}

export interface FileResult<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export function formatBytes(bytes: number, decimals: number = 2): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

export function readTextFile(filepath: string, options: ReadFileOptions = {}): FileResult<string> {
  const { encoding = 'utf-8', default: defaultValue } = options;
  try {
    if (!fs.existsSync(filepath)) {
      if (defaultValue !== undefined) {
        return { success: true, data: defaultValue as string };
      }
      return { success: false, error: `File not found: ${filepath}` };
    }
    const content = fs.readFileSync(filepath, encoding as BufferEncoding);
    return { success: true, data: content };
  } catch (err) {
    return { success: false, error: `Failed to read file: ${err instanceof Error ? err.message : String(err)}` };
  }
}

export function readBinaryFile(filepath: string, options: Omit<ReadFileOptions, 'encoding'> = {}): FileResult<Buffer> {
  const { default: defaultValue } = options;
  try {
    if (!fs.existsSync(filepath)) {
      if (defaultValue !== undefined) {
        return { success: true, data: defaultValue as Buffer };
      }
      return { success: false, error: `File not found: ${filepath}` };
    }
    const content = fs.readFileSync(filepath);
    return { success: true, data: content };
  } catch (err) {
    return { success: false, error: `Failed to read file: ${err instanceof Error ? err.message : String(err)}` };
  }
}

export function writeTextFile(filepath: string, content: string, options: WriteFileOptions = {}): FileResult<void> {
  const { encoding = 'utf-8', createDirs = true, atomic = false, mode = 0o644 } = options;
  try {
    const dir = path.dirname(filepath);
    if (createDirs && !fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    if (atomic) {
      const tempPath = filepath + '.tmp';
      fs.writeFileSync(tempPath, content, { encoding, mode });
      fs.renameSync(tempPath, filepath);
    } else {
      fs.writeFileSync(filepath, content, { encoding, mode });
    }
    return { success: true };
  } catch (err) {
    return { success: false, error: `Failed to write file: ${err instanceof Error ? err.message : String(err)}` };
  }
}

export function writeBinaryFile(filepath: string, content: Buffer, options: Omit<WriteFileOptions, 'encoding'> = {}): FileResult<void> {
  const { createDirs = true, atomic = false, mode = 0o644 } = options;
  try {
    const dir = path.dirname(filepath);
    if (createDirs && !fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    if (atomic) {
      const tempPath = filepath + '.tmp';
      fs.writeFileSync(tempPath, content, { mode });
      fs.renameSync(tempPath, filepath);
    } else {
      fs.writeFileSync(filepath, content, { mode });
    }
    return { success: true };
  } catch (err) {
    return { success: false, error: `Failed to write file: ${err instanceof Error ? err.message : String(err)}` };
  }
}

export function fileExists(filepath: string): boolean {
  return fs.existsSync(filepath);
}

export function isFile(filepath: string): FileResult<boolean> {
  try {
    const stats = fs.statSync(filepath);
    return { success: true, data: stats.isFile() };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function isDirectory(filepath: string): FileResult<boolean> {
  try {
    const stats = fs.statSync(filepath);
    return { success: true, data: stats.isDirectory() };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function getFileInfo(filepath: string): FileResult<FileInfo> {
  try {
    const stats = fs.statSync(filepath);
    const parsed = path.parse(filepath);
    return {
      success: true,
      data: {
        path: filepath,
        name: parsed.base,
        size: stats.size,
        sizeHuman: formatBytes(stats.size),
        isDirectory: stats.isDirectory(),
        isFile: stats.isFile(),
        isSymbolicLink: stats.isSymbolicLink(),
        created: stats.birthtime,
        modified: stats.mtime,
        accessed: stats.atime
      }
    };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function ensureDir(dirpath: string, mode: number = 0o755): FileResult<void> {
  try {
    if (!fs.existsSync(dirpath)) {
      fs.mkdirSync(dirpath, { recursive: true, mode });
    }
    return { success: true };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

function matchPattern(filename: string, pattern: string): boolean {
  const regex = new RegExp('^' + pattern.replace(/\./g, '\\.').replace(/\*/g, '.*').replace(/\?/g, '.') + '$');
  return regex.test(filename);
}

export function listFiles(dirpath: string, options: ListFilesOptions = {}): FileResult<FileInfo[]> {
  const { recursive = false, includeDirs = false, pattern, sortBy = 'name', order = 'asc' } = options;
  try {
    if (!fs.existsSync(dirpath)) {
      return { success: false, error: `Directory not found: ${dirpath}` };
    }
    const result: FileInfo[] = [];
    function scanDir(currentPath: string, isRecursive: boolean) {
      const entries = fs.readdirSync(currentPath, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(currentPath, entry.name);
        const stats = fs.statSync(fullPath);
        const isDir = stats.isDirectory();
        if (isDir && !includeDirs && !isRecursive) continue;
        if (pattern && !matchPattern(entry.name, pattern)) continue;
        const fileInfo: FileInfo = {
          path: fullPath,
          name: entry.name,
          size: stats.size,
          sizeHuman: formatBytes(stats.size),
          isDirectory: isDir,
          isFile: stats.isFile(),
          isSymbolicLink: stats.isSymbolicLink(),
          created: stats.birthtime,
          modified: stats.mtime,
          accessed: stats.atime
        };
        result.push(fileInfo);
        if (isDir && recursive) {
          scanDir(fullPath, true);
        }
      }
    }
    scanDir(dirpath, recursive);
    result.sort((a, b) => {
      let comparison = 0;
      switch (sortBy) {
        case 'size':
          comparison = a.size - b.size;
          break;
        case 'mtime':
          comparison = a.modified.getTime() - b.modified.getTime();
          break;
        case 'ctime':
          comparison = a.created.getTime() - b.created.getTime();
          break;
        case 'name':
        default:
          comparison = a.name.localeCompare(b.name);
      }
      return order === 'desc' ? -comparison : comparison;
    });
    return { success: true, data: result };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function copyFile(src: string, dest: string, overwrite: boolean = false): FileResult<void> {
  try {
    if (!fs.existsSync(src)) {
      return { success: false, error: `Source file not found: ${src}` };
    }
    if (fs.existsSync(dest) && !overwrite) {
      return { success: false, error: `Destination file already exists: ${dest}` };
    }
    const destDir = path.dirname(dest);
    if (!fs.existsSync(destDir)) {
      fs.mkdirSync(destDir, { recursive: true });
    }
    fs.copyFileSync(src, dest);
    return { success: true };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function moveFile(src: string, dest: string, overwrite: boolean = false): FileResult<void> {
  try {
    if (!fs.existsSync(src)) {
      return { success: false, error: `Source file not found: ${src}` };
    }
    if (fs.existsSync(dest) && !overwrite) {
      return { success: false, error: `Destination file already exists: ${dest}` };
    }
    const destDir = path.dirname(dest);
    if (!fs.existsSync(destDir)) {
      fs.mkdirSync(destDir, { recursive: true });
    }
    fs.renameSync(src, dest);
    return { success: true };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function deleteFile(filepath: string, missingOk: boolean = true): FileResult<void> {
  try {
    if (!fs.existsSync(filepath)) {
      if (missingOk) return { success: true };
      return { success: false, error: `File not found: ${filepath}` };
    }
    fs.unlinkSync(filepath);
    return { success: true };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function getFileHash(filepath: string, algorithm: 'md5' | 'sha1' | 'sha256' = 'sha256'): FileResult<string> {
  try {
    if (!fs.existsSync(filepath)) {
      return { success: false, error: `File not found: ${filepath}` };
    }
    const hash = createHash(algorithm);
    const data = fs.readFileSync(filepath);
    hash.update(data);
    return { success: true, data: hash.digest('hex') };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function getUniqueFilename(filepath: string, suffixFormat: string = '_{}'): FileResult<string> {
  try {
    if (!fs.existsSync(filepath)) {
      return { success: true, data: filepath };
    }
    const parsed = path.parse(filepath);
    let counter = 1;
    let newPath = filepath;
    while (fs.existsSync(newPath)) {
      const suffix = suffixFormat.replace('{}', String(counter));
      newPath = path.join(parsed.dir, parsed.name + suffix + parsed.ext);
      counter++;
    }
    return { success: true, data: newPath };
  } catch (err) {
    return { success: false, error: err instanceof Error ? err.message : String(err) };
  }
}

export function joinPaths(...paths: string[]): string {
  return path.join(...paths);
}

export function getExtension(filepath: string): string {
  return path.extname(filepath);
}

export function getBasename(filepath: string, ext?: string): string {
  return path.basename(filepath, ext);
}

export function getDirname(filepath: string): string {
  return path.dirname(filepath);
}

export function resolvePath(filepath: string): string {
  return path.resolve(filepath);
}

export function normalizePath(filepath: string): string {
  return path.normalize(filepath);
}

export function isAbsolutePath(filepath: string): boolean {
  return path.isAbsolute(filepath);
}

export function getRelativePath(from: string, to: string): string {
  return path.relative(from, to);
}

