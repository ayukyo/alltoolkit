/**
 * Pagination Utilities - JavaScript 分页工具
 * 
 * 提供完整的分页实现，包括：
 * - 基于偏移量的分页 (Offset Pagination)
 * - 基于游标的分页 (Cursor Pagination)
 * - 基于键集的分页 (Keyset Pagination)
 * - 无限滚动分页 (Infinite Scroll)
 * - 分页元数据生成
 * - 分页链接生成
 * 
 * 零外部依赖，纯 JavaScript 实现。
 */

/**
 * 分页类型枚举
 */
const PaginationType = {
  OFFSET: 'offset',
  CURSOR: 'cursor',
  KEYSET: 'keyset',
  INFINITE: 'infinite'
};

/**
 * 创建分页元数据
 * @param {Object} options - 元数据选项
 * @returns {Object} 分页元数据
 */
function createPageMetadata(options) {
  const {
    currentPage = 1,
    totalPages = 1,
    totalItems = 0,
    itemsPerPage = 20,
    hasPrevious = false,
    hasNext = false,
    previousPage = null,
    nextPage = null,
    firstPage = 1,
    lastPage = 1,
    startIndex = 0,
    endIndex = 0
  } = options;

  return {
    currentPage,
    totalPages,
    totalItems,
    itemsPerPage,
    hasPrevious,
    hasNext,
    previousPage,
    nextPage,
    firstPage,
    lastPage,
    startIndex,
    endIndex,
    toJSON() {
      return {
        currentPage: this.currentPage,
        totalPages: this.totalPages,
        totalItems: this.totalItems,
        itemsPerPage: this.itemsPerPage,
        hasPrevious: this.hasPrevious,
        hasNext: this.hasNext,
        previousPage: this.previousPage,
        nextPage: this.nextPage,
        firstPage: this.firstPage,
        lastPage: this.lastPage,
        startIndex: this.startIndex,
        endIndex: this.endIndex
      };
    }
  };
}

/**
 * 创建游标分页元数据
 * @param {Object} options - 元数据选项
 * @returns {Object} 游标元数据
 */
function createCursorMetadata(options) {
  const {
    cursor = null,
    nextCursor = null,
    previousCursor = null,
    hasMore = false,
    limit = 20
  } = options;

  return {
    cursor,
    nextCursor,
    previousCursor,
    hasMore,
    limit,
    toJSON() {
      return {
        cursor: this.cursor,
        nextCursor: this.nextCursor,
        previousCursor: this.previousCursor,
        hasMore: this.hasMore,
        limit: this.limit
      };
    }
  };
}

/**
 * 创建分页结果
 * @param {Array} items - 数据项
 * @param {Object} metadata - 元数据
 * @param {string} paginationType - 分页类型
 * @returns {Object} 分页结果
 */
function createPaginatedResult(items, metadata, paginationType) {
  return {
    items,
    metadata,
    paginationType,
    toJSON() {
      return {
        items: this.items,
        pagination: this.metadata.toJSON(),
        type: this.paginationType
      };
    }
  };
}

/**
 * 基于偏移量的分页器
 * 
 * 最传统的分页方式，适用于：
 * - 需要显示总页数
 * - 可以跳转到任意页
 * - 数据集相对较小
 */
class OffsetPaginator {
  /**
   * @param {Object} options - 配置选项
   * @param {number} [options.itemsPerPage=20] - 每页默认数量
   * @param {number} [options.maxItemsPerPage=100] - 每页最大数量
   * @param {number} [options.minItemsPerPage=1] - 每页最小数量
   */
  constructor(options = {}) {
    const {
      itemsPerPage = 20,
      maxItemsPerPage = 100,
      minItemsPerPage = 1
    } = options;

    this.itemsPerPage = Math.max(minItemsPerPage, Math.min(itemsPerPage, maxItemsPerPage));
    this.maxItemsPerPage = maxItemsPerPage;
    this.minItemsPerPage = minItemsPerPage;
  }

  /**
   * 对数组进行分页
   * @param {Array} items - 要分页的数组
   * @param {number} [page=1] - 页码（从 1 开始）
   * @param {number} [perPage] - 每页数量（可选）
   * @returns {Object} 分页结果
   */
  paginate(items, page = 1, perPage) {
    // 处理每页数量
    let itemsPerPage = perPage ?? this.itemsPerPage;
    itemsPerPage = Math.max(this.minItemsPerPage, Math.min(itemsPerPage, this.maxItemsPerPage));

    const totalItems = items.length;

    // 边界处理：空数组快速返回
    if (totalItems === 0) {
      return createPaginatedResult(
        [],
        createPageMetadata({
          currentPage: 1,
          totalPages: 1,
          totalItems: 0,
          itemsPerPage,
          hasPrevious: false,
          hasNext: false
        }),
        PaginationType.OFFSET
      );
    }

    // 计算总页数（使用整数运算）
    let totalPages;
    if (totalItems <= itemsPerPage) {
      totalPages = 1;
    } else {
      totalPages = Math.ceil(totalItems / itemsPerPage);
    }

    // 边界处理：单页快速返回
    if (totalPages === 1) {
      return createPaginatedResult(
        [...items],
        createPageMetadata({
          currentPage: 1,
          totalPages: 1,
          totalItems,
          itemsPerPage,
          hasPrevious: false,
          hasNext: false,
          startIndex: 1,
          endIndex: totalItems
        }),
        PaginationType.OFFSET
      );
    }

    // 处理边界页码
    if (page < 1) page = 1;
    if (page > totalPages) page = totalPages;

    // 计算偏移量
    const offset = (page - 1) * itemsPerPage;

    // 切片获取当前页数据
    const pageItems = items.slice(offset, offset + itemsPerPage);

    // 计算元数据
    const hasPrevious = page > 1;
    const hasNext = page < totalPages;
    const startIndex = pageItems.length > 0 ? offset + 1 : 0;
    const endIndex = offset + pageItems.length;

    return createPaginatedResult(
      pageItems,
      createPageMetadata({
        currentPage: page,
        totalPages,
        totalItems,
        itemsPerPage,
        hasPrevious,
        hasNext,
        previousPage: hasPrevious ? page - 1 : null,
        nextPage: hasNext ? page + 1 : null,
        firstPage: 1,
        lastPage: totalPages,
        startIndex,
        endIndex
      }),
      PaginationType.OFFSET
    );
  }

  /**
   * 获取 SQL 查询用的 OFFSET 和 LIMIT
   * @param {number} page - 页码
   * @param {number} [perPage] - 每页数量
   * @returns {Object} { offset, limit }
   */
  getOffsetLimit(page, perPage) {
    let itemsPerPage = perPage ?? this.itemsPerPage;
    itemsPerPage = Math.max(this.minItemsPerPage, Math.min(itemsPerPage, this.maxItemsPerPage));
    return {
      offset: (page - 1) * itemsPerPage,
      limit: itemsPerPage
    };
  }

  /**
   * 计算总页数
   * @param {number} totalItems - 总条目数
   * @param {number} [perPage] - 每页数量
   * @returns {number} 总页数
   */
  calculatePages(totalItems, perPage) {
    if (totalItems <= 0) return 1;

    let itemsPerPage = perPage ?? this.itemsPerPage;
    itemsPerPage = Math.max(this.minItemsPerPage, Math.min(itemsPerPage, this.maxItemsPerPage));

    if (totalItems <= itemsPerPage) return 1;
    return Math.ceil(totalItems / itemsPerPage);
  }
}

/**
 * 基于游标的分页器
 * 
 * 适用于：
 * - 大数据集
 * - 实时数据流
 * - API 设计 (GraphQL, REST)
 * - 无限滚动
 */
class CursorPaginator {
  /**
   * @param {Object} options - 配置选项
   * @param {number} [options.limit=20] - 每页默认数量
   * @param {number} [options.maxLimit=100] - 每页最大数量
   * @param {number} [options.minLimit=1] - 每页最小数量
   * @param {Function} [options.cursorEncoder] - 自定义游标编码器
   * @param {Function} [options.cursorDecoder] - 自定义游标解码器
   */
  constructor(options = {}) {
    const {
      limit = 20,
      maxLimit = 100,
      minLimit = 1,
      cursorEncoder,
      cursorDecoder
    } = options;

    this.limit = Math.max(minLimit, Math.min(limit, maxLimit));
    this.maxLimit = maxLimit;
    this.minLimit = minLimit;

    // 默认编码器：JSON -> Base64
    this._encoder = cursorEncoder || this._defaultEncode.bind(this);
    this._decoder = cursorDecoder || this._defaultDecode.bind(this);
  }

  _defaultEncode(data) {
    const jsonStr = JSON.stringify(data);
    if (typeof Buffer !== 'undefined') {
      return Buffer.from(jsonStr).toString('base64url');
    }
    // 浏览器环境
    return btoa(jsonStr).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }

  _defaultDecode(cursor) {
    try {
      let jsonStr;
      if (typeof Buffer !== 'undefined') {
        jsonStr = Buffer.from(cursor, 'base64url').toString();
      } else {
        // 浏览器环境
        jsonStr = atob(cursor.replace(/-/g, '+').replace(/_/g, '/'));
      }
      return JSON.parse(jsonStr);
    } catch {
      return {};
    }
  }

  /**
   * 编码游标
   * @param {number} index - 索引位置
   * @param {string} [direction='next'] - 方向
   * @returns {string} 编码后的游标
   */
  encodeCursor(index, direction = 'next') {
    return this._encoder({ index, direction });
  }

  /**
   * 解码游标
   * @param {string} cursor - 游标字符串
   * @returns {Object} 包含索引和方向的对象
   */
  decodeCursor(cursor) {
    return this._decoder(cursor);
  }

  /**
   * 对数组进行游标分页
   * @param {Array} items - 要分页的数组
   * @param {string} [cursor] - 游标字符串
   * @param {number} [limit] - 每页数量
   * @param {string} [direction='next'] - 方向
   * @returns {Object} 分页结果
   */
  paginate(items, cursor, limit, direction = 'next') {
    // 处理每页数量
    let pageLimit = limit ?? this.limit;
    pageLimit = Math.max(this.minLimit, Math.min(pageLimit, this.maxLimit));

    const totalItems = items.length;

    // 解析游标
    let startIndex = 0;
    if (cursor) {
      const cursorData = this.decodeCursor(cursor);
      startIndex = cursorData.index || 0;
      direction = cursorData.direction || direction;
    }

    // 根据方向获取数据
    let pageItems;
    let nextIndex;
    let prevIndex;
    let endIndex;

    if (direction === 'next') {
      endIndex = Math.min(startIndex + pageLimit, totalItems);
      pageItems = items.slice(startIndex, endIndex);
      nextIndex = endIndex;
      prevIndex = startIndex;
    } else {
      // 向前翻页
      startIndex = Math.max(0, startIndex - pageLimit);
      endIndex = startIndex + pageLimit;
      pageItems = items.slice(startIndex, endIndex);
      nextIndex = endIndex;
      prevIndex = startIndex;
    }

    // 判断是否有更多数据
    const hasMoreNext = endIndex < totalItems;
    const hasMorePrev = startIndex > 0;

    // 生成游标
    const nextCursor = hasMoreNext ? this.encodeCursor(nextIndex, 'next') : null;
    const prevCursor = hasMorePrev ? this.encodeCursor(prevIndex, 'previous') : null;

    return createPaginatedResult(
      pageItems,
      createCursorMetadata({
        cursor,
        nextCursor,
        previousCursor: prevCursor,
        hasMore: direction === 'next' ? hasMoreNext : hasMorePrev,
        limit: pageLimit
      }),
      PaginationType.CURSOR
    );
  }

  /**
   * 获取第一页
   * @param {Array} items - 数据数组
   * @param {number} [limit] - 每页数量
   * @returns {Object} 分页结果
   */
  getFirstPage(items, limit) {
    return this.paginate(items, null, limit, 'next');
  }
}

/**
 * 基于键集的分页器
 * 
 * 适用于：
 * - 数据库查询优化
 * - 按特定字段排序的分页
 * - 大数据集的高效分页
 */
class KeysetPaginator {
  /**
   * @param {Object} options - 配置选项
   * @param {number} [options.limit=20] - 每页默认数量
   * @param {number} [options.maxLimit=100] - 每页最大数量
   * @param {string} [options.keyField='id'] - 键字段名
   * @param {Function} [options.keyExtractor] - 从 item 提取键的函数
   */
  constructor(options = {}) {
    const {
      limit = 20,
      maxLimit = 100,
      keyField = 'id',
      keyExtractor
    } = options;

    this.limit = Math.min(limit, maxLimit);
    this.maxLimit = maxLimit;
    this.keyField = keyField;
    this.keyExtractor = keyExtractor;
  }

  _getKey(item) {
    if (this.keyExtractor) {
      return this.keyExtractor(item);
    }
    if (typeof item === 'object' && item !== null) {
      return item[this.keyField];
    }
    return item;
  }

  /**
   * 编码键为游标
   * @param {*} key - 键值
   * @returns {string} 游标
   */
  encodeCursor(key) {
    try {
      const keyStr = JSON.stringify(key);
      if (typeof Buffer !== 'undefined') {
        return Buffer.from(keyStr).toString('base64url');
      }
      return btoa(keyStr).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    } catch {
      // 对于非 JSON 可序列化的键，使用字符串
      const keyStr = String(key);
      if (typeof Buffer !== 'undefined') {
        return Buffer.from(keyStr).toString('base64url');
      }
      return btoa(keyStr).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    }
  }

  /**
   * 解码游标为键
   * @param {string} cursor - 游标
   * @returns {*} 键值
   */
  decodeCursor(cursor) {
    try {
      let keyStr;
      if (typeof Buffer !== 'undefined') {
        keyStr = Buffer.from(cursor, 'base64url').toString();
      } else {
        keyStr = atob(cursor.replace(/-/g, '+').replace(/_/g, '/'));
      }
      return JSON.parse(keyStr);
    } catch {
      return cursor;
    }
  }

  /**
   * 对数组进行键集分页
   * @param {Array} items - 要分页的数组（应已按键排序）
   * @param {string} [cursor] - 游标字符串
   * @param {number} [limit] - 每页数量
   * @param {boolean} [descending=false] - 是否降序
   * @returns {Object} 分页结果
   */
  paginate(items, cursor, limit, descending = false) {
    let pageLimit = limit ?? this.limit;
    pageLimit = Math.min(pageLimit, this.maxLimit);

    // 解析游标
    let lastKey = null;
    if (cursor) {
      lastKey = this.decodeCursor(cursor);
    }

    // 找到起始位置
    let startIndex = 0;
    if (lastKey !== null) {
      for (let i = 0; i < items.length; i++) {
        const key = this._getKey(items[i]);
        if (descending) {
          if (key < lastKey) {
            startIndex = i;
            break;
          }
        } else {
          if (key > lastKey) {
            startIndex = i;
            break;
          }
        }
      }
    }

    // 切片
    const endIndex = Math.min(startIndex + pageLimit, items.length);
    const pageItems = items.slice(startIndex, endIndex);

    // 判断是否有更多
    const hasMore = endIndex < items.length;

    // 生成下一页游标
    let nextCursor = null;
    if (pageItems.length > 0 && hasMore) {
      const lastItemKey = this._getKey(pageItems[pageItems.length - 1]);
      nextCursor = this.encodeCursor(lastItemKey);
    }

    return createPaginatedResult(
      pageItems,
      createCursorMetadata({
        cursor,
        nextCursor,
        previousCursor: null, // 键集分页通常不支持反向
        hasMore,
        limit: pageLimit
      }),
      PaginationType.KEYSET
    );
  }
}

/**
 * 无限滚动分页器
 * 
 * 适用于：
 * - 社交媒体时间线
 * - 新闻列表
 * - 图片/视频瀑布流
 */
class InfiniteScrollPaginator {
  /**
   * @param {Object} options - 配置选项
   * @param {number} [options.batchSize=20] - 每批次数量
   * @param {number} [options.maxBatchSize=50] - 最大批次数量
   * @param {number} [options.preloadThreshold=5] - 预加载阈值
   */
  constructor(options = {}) {
    const {
      batchSize = 20,
      maxBatchSize = 50,
      preloadThreshold = 5
    } = options;

    this.batchSize = Math.min(batchSize, maxBatchSize);
    this.maxBatchSize = maxBatchSize;
    this.preloadThreshold = preloadThreshold;
  }

  /**
   * 获取下一批次
   * @param {Array} items - 全部数据数组
   * @param {number} [loadedCount=0] - 已加载数量
   * @param {number} [batchSize] - 本次加载数量
   * @returns {Object} 分页结果
   */
  paginate(items, loadedCount = 0, batchSize) {
    const size = Math.min(batchSize ?? this.batchSize, this.maxBatchSize);

    // 计算本次加载范围
    const startIndex = loadedCount;
    const endIndex = Math.min(startIndex + size, items.length);

    const batchItems = items.slice(startIndex, endIndex);

    // 是否需要预加载
    const remaining = items.length - endIndex;
    const shouldPreload = remaining <= this.preloadThreshold && remaining > 0;

    const hasMore = endIndex < items.length;

    return createPaginatedResult(
      batchItems,
      createCursorMetadata({
        cursor: String(loadedCount),
        nextCursor: hasMore ? String(endIndex) : null,
        previousCursor: null,
        hasMore,
        limit: size
      }),
      PaginationType.INFINITE
    );
  }

  /**
   * 获取加载状态
   * @param {number} totalItems - 总条目数
   * @param {number} loadedCount - 已加载数量
   * @returns {Object} 状态对象
   */
  getLoadState(totalItems, loadedCount) {
    const remaining = totalItems - loadedCount;
    const progress = totalItems > 0 ? loadedCount / totalItems : 1.0;

    return {
      total: totalItems,
      loaded: loadedCount,
      remaining,
      progress: Math.round(progress * 100) / 100,
      shouldPreload: remaining <= this.preloadThreshold && remaining > 0,
      isComplete: loadedCount >= totalItems
    };
  }
}

/**
 * 分页高级接口
 */
const Pagination = {
  /**
   * 基于偏移量的分页
   * @param {Array} items - 数据数组
   * @param {number} [page=1] - 页码
   * @param {number} [perPage=20] - 每页数量
   * @returns {Object} 分页结果
   */
  offset(items, page = 1, perPage = 20) {
    const paginator = new OffsetPaginator({ itemsPerPage: perPage });
    return paginator.paginate(items, page, perPage);
  },

  /**
   * 基于游标的分页
   * @param {Array} items - 数据数组
   * @param {string} [cursor] - 游标
   * @param {number} [limit=20] - 每页数量
   * @returns {Object} 分页结果
   */
  cursor(items, cursor, limit = 20) {
    const paginator = new CursorPaginator({ limit });
    return paginator.paginate(items, cursor, limit);
  },

  /**
   * 基于键集的分页
   * @param {Array} items - 数据数组（应已排序）
   * @param {string} [cursor] - 游标
   * @param {number} [limit=20] - 每页数量
   * @param {string} [keyField='id'] - 键字段
   * @returns {Object} 分页结果
   */
  keyset(items, cursor, limit = 20, keyField = 'id') {
    const paginator = new KeysetPaginator({ limit, keyField });
    return paginator.paginate(items, cursor, limit);
  },

  /**
   * 无限滚动分页
   * @param {Array} items - 数据数组
   * @param {number} [loadedCount=0] - 已加载数量
   * @param {number} [batchSize=20] - 每批数量
   * @returns {Object} 分页结果
   */
  infinite(items, loadedCount = 0, batchSize = 20) {
    const paginator = new InfiniteScrollPaginator({ batchSize });
    return paginator.paginate(items, loadedCount, batchSize);
  },

  /**
   * 计算显示的页码范围
   * @param {number} currentPage - 当前页
   * @param {number} totalPages - 总页数
   * @param {number} [maxDisplay=7] - 最多显示页数
   * @returns {number[]} 要显示的页码数组
   */
  calculatePageRange(currentPage, totalPages, maxDisplay = 7) {
    // 边界处理
    if (totalPages <= 0 || currentPage <= 0 || maxDisplay <= 0) {
      return [];
    }

    // 快速路径：总页数不超过显示数
    if (totalPages <= maxDisplay) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    // 快速路径：单页
    if (totalPages === 1) {
      return [1];
    }

    // 边界处理：当前页超出范围
    let page = currentPage;
    if (page > totalPages) page = totalPages;
    if (page < 1) page = 1;

    // 计算范围
    const halfDisplay = Math.floor(maxDisplay / 2);
    let start = Math.max(1, page - halfDisplay);
    let end = start + maxDisplay - 1;

    // 边界调整：末尾超出时从右往左计算
    if (end > totalPages) {
      end = totalPages;
      start = Math.max(1, end - maxDisplay + 1);
    }

    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  },

  /**
   * 生成分页链接
   * @param {string} baseUrl - 基础 URL
   * @param {number} currentPage - 当前页
   * @param {number} totalPages - 总页数
   * @param {string} [pageParam='page'] - 页码参数名
   * @returns {Object} 包含各页链接的对象
   */
  generateLinks(baseUrl, currentPage, totalPages, pageParam = 'page') {
    // 边界处理
    if (currentPage <= 0 || totalPages <= 0) {
      return {};
    }

    // 预构建 URL 模板
    const urlTemplate = `${baseUrl}?${pageParam}=`;

    const links = {};

    // 第一页和最后一页
    links.first = `${urlTemplate}1`;
    links.last = `${urlTemplate}${totalPages}`;

    // 上一页
    if (currentPage > 1) {
      links.prev = `${urlTemplate}${currentPage - 1}`;
    }

    // 下一页
    if (currentPage < totalPages) {
      links.next = `${urlTemplate}${currentPage + 1}`;
    }

    // 当前页
    links.self = `${urlTemplate}${currentPage}`;

    return links;
  },

  /**
   * 生成 HTTP Link Header 格式
   * @param {string} baseUrl - 基础 URL
   * @param {number} currentPage - 当前页
   * @param {number} totalPages - 总页数
   * @param {string} [pageParam='page'] - 页码参数名
   * @returns {string} Link Header 字符串
   */
  generateHeaderLinks(baseUrl, currentPage, totalPages, pageParam = 'page') {
    const links = this.generateLinks(baseUrl, currentPage, totalPages, pageParam);
    return Object.entries(links)
      .map(([rel, url]) => `<${url}>; rel="${rel}"`)
      .join(', ');
  }
};

// 便捷函数
const paginateOffset = (items, page = 1, perPage = 20) => Pagination.offset(items, page, perPage);
const paginateCursor = (items, cursor, limit = 20) => Pagination.cursor(items, cursor, limit);
const paginateInfinite = (items, loaded = 0, batch = 20) => Pagination.infinite(items, loaded, batch);
const pageRange = (current, total, maxDisplay = 7) => Pagination.calculatePageRange(current, total, maxDisplay);

// 导出
module.exports = {
  // 类型
  PaginationType,
  
  // 类
  OffsetPaginator,
  CursorPaginator,
  KeysetPaginator,
  InfiniteScrollPaginator,
  
  // 高级接口
  Pagination,
  
  // 便捷函数
  paginateOffset,
  paginateCursor,
  paginateInfinite,
  pageRange,
  
  // 工厂函数
  createPageMetadata,
  createCursorMetadata,
  createPaginatedResult
};