class Remedian
  def initialize(base, ntile = 50)
    @base = base
    @exponent = 1
    @ntile = ntile
    @storage = Array.new
    @positions = Array.new
    @storage << Array.new
    @positions << 0
  end

  def self.quickselect(a, k)
    arr = a.dup
    loop do
      pivot = arr.delete_at(rand(arr.length))
      left, right = arr.partition { |x| x < pivot }
      if k == left.length
        return pivot
      elsif k < left.length
        arr = left
      else
        k = k - left.length - 1
        arr = right
      end
    end
  end

  def next(element, level = 0)
    if level >= @exponent
      @exponent = @exponent + 1
      @positions << 0
      @storage << Array.new
    end
    begin
      @storage[level][@positions[level]] = element
      if @positions[level] < @base - 1
        @positions[level] = @positions[level] + 1
      else
        @positions[level] = 0
        if level == 0
          self.next(Remedian::quickselect(@storage[level], (@storage[level].length * @ntile)/100), level + 1)
        else
          self.next(Remedian::quickselect(@storage[level], @storage[level].length/2), level + 1)
        end
      end
    rescue StandardError => e
      p 'error at %d' % element
      abort(e.message)

    end
  end

  def result()
    weighted_total = 0
    total_weight = 0
    weight = 1
    @storage.each do |a|
      a.each do |v|
        total_weight = total_weight + weight
        weighted_total = weighted_total + v*weight
      end
      weight = weight * @base
    end
    weighted_total/total_weight
  end
end

ntile = 50
set_size = 2000
base = 101

r = Remedian.new(base, ntile)

1.upto set_size do |num|
  r.next(num)
end

p 'sequential result: %d' % r.result
top = set_size
bottom = 1

r = Remedian.new(base, ntile)

loop do
6.times do
  r.next(top)
  top = top - 1
  break if top < bottom
end
break if top < bottom
5.times do
  r.next(bottom)
  bottom = bottom + 1
  break if top < bottom
end
break if top < bottom
end

p 'worst case result: %d' % r.result

p '10 random results:'

10.times do
  r = Remedian.new(base, ntile)
  a = *(1..set_size)
  while a.length > 0 do
    r.next(a.delete_at(rand(a.length)))
  end
  p r.result
end

p 'distribution of 10,000 random results:'

result_counts = Hash.new 0

10000.times do
  r = Remedian.new(base, ntile)
  a = *(1..set_size)
  while a.length > 0 do
    r.next(a.delete_at(rand(a.length)))
  end
  result_counts[r.result] += 1
end

result_counts.keys.sort.each do |k|
  p '%d: %d' % [k, result_counts[k]]
end